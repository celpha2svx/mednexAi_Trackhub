from django.db import models
from django.conf import settings


class InviteCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='invite_code'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "used" if self.used_by else ("active" if self.is_active else "inactive")
        return f"{self.code} [{status}]"


class Report(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    date = models.DateField(auto_now_add=False, default=None, null=True, blank=True)
    report_day = models.PositiveIntegerField(
        help_text="Sequential day number (e.g., 1, 2, 8)"
    )
    hours_today = models.DecimalField(max_digits=3, decimal_places=1)
    hours_total = models.DecimalField(max_digits=4, decimal_places=1)
    task_description = models.TextField()
    discipline_score = models.PositiveIntegerField()
    discipline_max = models.PositiveIntegerField()
    visibility_status = models.BooleanField(default=False, verbose_name="Posted Status Update")
    visibility_twitter = models.BooleanField(default=False, verbose_name="Posted on Twitter/X")
    visibility_comment = models.BooleanField(default=False, verbose_name="Left a Comment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-report_day']
        unique_together = ('user', 'report_day')

    def __str__(self):
        return f"{self.user.username} - Day {self.report_day} ({self.date})"

    @property
    def discipline_percentage(self):
        if self.discipline_max == 0:
            return 0
        return round((self.discipline_score / self.discipline_max) * 100)
