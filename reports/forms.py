from django import forms
from .models import Report

INPUT_CLASS = 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-indigo-400'
CHECKBOX_CLASS = 'h-4 w-4 text-indigo-600 border-gray-300 rounded'


class ReportForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    class Meta:
        model = Report
        exclude = ('user', 'date', 'created_at')
        widgets = {
            'report_day': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1}),
            'hours_today': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.5', 'min': 0}),
            'hours_total': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.5', 'min': 0}),
            'task_description': forms.Textarea(attrs={'rows': 5, 'class': INPUT_CLASS, 'placeholder': 'What did you work on today?'}),
            'discipline_score': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 0}),
            'discipline_max': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1}),
            'visibility_status': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASS}),
            'visibility_twitter': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASS}),
            'visibility_comment': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASS}),
        }
        labels = {
            'report_day': 'Day Number',
            'hours_today': "Hours Studied Today",
            'hours_total': "Total Hours So Far",
            'task_description': "What did you work on?",
            'discipline_score': "Discipline Score",
            'discipline_max': "Max Possible Score",
        }
        help_texts = {
            'report_day': 'The sequential day of your learning journey (e.g. Day 1, Day 30)',
            'discipline_score': 'Your self-rated discipline for today',
            'discipline_max': 'Maximum score you set for yourself',
        }

    def clean(self):
        cleaned = super().clean()
        score = cleaned.get('discipline_score')
        max_score = cleaned.get('discipline_max')
        if score and max_score and score > max_score:
            raise forms.ValidationError("Discipline score cannot exceed the maximum score.")
        hours_today = cleaned.get('hours_today')
        hours_total = cleaned.get('hours_total')
        if hours_today and hours_total and hours_today > hours_total:
            raise forms.ValidationError("Hours today cannot exceed total hours.")
        # Check duplicate day for this user
        report_day = cleaned.get('report_day')
        if self._user and report_day:
            if Report.objects.filter(user=self._user, report_day=report_day).exists():
                raise forms.ValidationError(
                    f"You already submitted a report for Day {report_day}. Each day can only be submitted once."
                )
        return cleaned
