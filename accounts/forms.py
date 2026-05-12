from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from reports.models import InviteCode


class RegisterForm(UserCreationForm):
    invite_code = forms.CharField(max_length=20, help_text="Enter the invite code provided by your mentor.")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'invite_code')

    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code')
        try:
            invite = InviteCode.objects.get(code=code, is_active=True, used_by__isnull=True)
        except InviteCode.DoesNotExist:
            raise forms.ValidationError("Invalid or already used invite code.")
        return code

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'learner'
        if commit:
            user.save()
            # Mark invite code as used
            code = self.cleaned_data['invite_code']
            InviteCode.objects.filter(code=code).update(is_active=False, used_by=user)
        return user
