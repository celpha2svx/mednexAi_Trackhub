from datetime import date, timedelta
from django.db.models import Count
from .models import Report


def get_user_streak(user):
    """Count consecutive days the user has submitted a report, ending today."""
    today = date.today()
    streak = 0
    check_date = today
    while True:
        if Report.objects.filter(user=user, date=check_date).exists():
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    return streak


def get_user_activity_30d(user):
    """Return percentage of last 30 days that user submitted a report."""
    start = date.today() - timedelta(days=29)
    active_days = Report.objects.filter(user=user, date__gte=start).count()
    return round((active_days / 30) * 100, 1)


def get_team_daily_counts(days=30):
    """Return list of {date, count} dicts for last N days — used in Chart.js."""
    start = date.today() - timedelta(days=days - 1)
    raw = list(
        Report.objects.filter(date__gte=start)
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    # Convert date objects to strings for JSON serialisation
    return [{'date': str(r['date']), 'count': r['count']} for r in raw]


def get_all_user_stats(users):
    """Return per-user stats dict for the mentor dashboard."""
    return {
        u.id: {
            'streak': get_user_streak(u),
            'activity_30d': get_user_activity_30d(u),
            'total_reports': Report.objects.filter(user=u).count(),
        }
        for u in users
    }
