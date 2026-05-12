import secrets
from django.contrib import admin
from django.utils.html import format_html
from .models import Report, InviteCode


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active', 'used_by', 'created_at')
    list_filter = ('is_active',)
    readonly_fields = ('used_by', 'created_at')
    actions = ['generate_codes']

    @admin.action(description='Generate 10 new invite codes')
    def generate_codes(self, request, queryset):
        created = 0
        for _ in range(10):
            code = secrets.token_urlsafe(8)
            InviteCode.objects.get_or_create(code=code)
            created += 1
        self.message_user(request, f"{created} invite codes generated.")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_day', 'date', 'hours_today', 'hours_total', 'discipline_badge', 'created_at')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'task_description')
    ordering = ('-date', '-report_day')

    def discipline_badge(self, obj):
        pct = obj.discipline_percentage
        color = 'green' if pct >= 80 else 'orange' if pct >= 50 else 'red'
        return format_html('<span style="color:{}">{}/{} ({}%)</span>', color, obj.discipline_score, obj.discipline_max, pct)
    discipline_badge.short_description = 'Discipline'
