import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Report
from .forms import ReportForm
from .utils import get_user_streak, get_team_daily_counts, get_all_user_stats
from accounts.models import CustomUser


class SubmitReportView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/submit.html'
    success_url = reverse_lazy('feed')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        from datetime import date
        form.instance.user = self.request.user
        form.instance.date = date.today()
        messages.success(self.request, "✅ Report submitted! Keep the streak alive 🔥")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below.")
        return super().form_invalid(form)


class FeedView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/feed.html'
    context_object_name = 'reports'
    paginate_by = 15

    def get_queryset(self):
        return Report.objects.select_related('user').order_by('-date', '-report_day')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_streak'] = get_user_streak(self.request.user)
        return ctx


class MentorDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'reports/dashboard.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.role == 'mentor'

    def get_queryset(self):
        return CustomUser.objects.filter(role='learner').order_by('username')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        learners = self.get_queryset()
        ctx['daily_data'] = json.dumps(get_team_daily_counts())
        ctx['user_stats'] = get_all_user_stats(learners)
        ctx['total_reports'] = Report.objects.count()
        ctx['total_learners'] = learners.count()
        return ctx
