import pytest
from datetime import date
from django.urls import reverse
from reports.models import InviteCode, Report
from reports.utils import get_user_streak
from django.contrib.auth import get_user_model

User = get_user_model()


# ─── Test 1: Invite Code Validation ────────────────────────────────────────

@pytest.mark.django_db
def test_valid_invite_code_allows_registration(client):
    InviteCode.objects.create(code='VALID123', is_active=True)
    response = client.post(reverse('register'), {
        'username': 'newuser',
        'email': 'new@test.com',
        'password1': 'Str0ngP@ss!',
        'password2': 'Str0ngP@ss!',
        'invite_code': 'VALID123',
    })
    assert response.status_code == 302  # Redirected after registration
    assert User.objects.filter(username='newuser').exists()
    assert not InviteCode.objects.get(code='VALID123').is_active  # Code consumed


@pytest.mark.django_db
def test_invalid_invite_code_blocks_registration(client):
    response = client.post(reverse('register'), {
        'username': 'newuser2',
        'email': 'new2@test.com',
        'password1': 'Str0ngP@ss!',
        'password2': 'Str0ngP@ss!',
        'invite_code': 'WRONGCODE',
    })
    assert response.status_code == 200  # Stays on form page
    assert not User.objects.filter(username='newuser2').exists()


@pytest.mark.django_db
def test_used_invite_code_is_rejected(client):
    user = User.objects.create_user(username='olduser', password='pass')
    InviteCode.objects.create(code='USEDCODE', is_active=False, used_by=user)
    response = client.post(reverse('register'), {
        'username': 'newuser3',
        'email': 'x@test.com',
        'password1': 'Str0ngP@ss!',
        'password2': 'Str0ngP@ss!',
        'invite_code': 'USEDCODE',
    })
    assert not User.objects.filter(username='newuser3').exists()


# ─── Test 2: Report Submission ──────────────────────────────────────────────

@pytest.mark.django_db
def test_learner_can_submit_report(client, learner_user):
    client.force_login(learner_user)
    response = client.post(reverse('submit'), {
        'report_day': 1,
        'hours_today': '2.5',
        'hours_total': '10.0',
        'task_description': 'Studied Django CBVs and wrote tests.',
        'discipline_score': 8,
        'discipline_max': 10,
        'visibility_status': True,
        'visibility_twitter': False,
        'visibility_comment': False,
    })
    assert response.status_code == 302
    assert Report.objects.filter(user=learner_user, report_day=1).exists()


@pytest.mark.django_db
def test_report_requires_login(client):
    response = client.get(reverse('submit'))
    assert response.status_code == 302
    assert 'next' in response['Location']  # Redirected with ?next= param


@pytest.mark.django_db
def test_duplicate_report_day_rejected(client, learner_user):
    Report.objects.create(
        user=learner_user,
        report_day=5,
        date=date.today(),
        hours_today=3,
        hours_total=15,
        task_description='Already submitted',
        discipline_score=7,
        discipline_max=10,
    )
    client.force_login(learner_user)
    response = client.post(reverse('submit'), {
        'report_day': 5,
        'hours_today': '2.0',
        'hours_total': '17.0',
        'task_description': 'Duplicate day.',
        'discipline_score': 6,
        'discipline_max': 10,
    })
    # Form should re-render (200) with validation error, not crash (500)
    assert response.status_code == 200
    assert Report.objects.filter(user=learner_user, report_day=5).count() == 1


# ─── Test 3: Streak Calculation ─────────────────────────────────────────────

@pytest.mark.django_db
def test_streak_counts_consecutive_days(learner_user):
    from datetime import timedelta
    today = date.today()
    for i in range(3):
        Report.objects.create(
            user=learner_user,
            date=today - timedelta(days=i),
            report_day=10 - i,
            hours_today=2,
            hours_total=10,
            task_description='Study',
            discipline_score=8,
            discipline_max=10,
        )
    assert get_user_streak(learner_user) == 3


@pytest.mark.django_db
def test_streak_breaks_on_gap(learner_user):
    from datetime import timedelta
    today = date.today()
    # Submit today and 2 days ago (skip yesterday)
    for i, day_offset in enumerate([0, 2]):
        Report.objects.create(
            user=learner_user,
            date=today - timedelta(days=day_offset),
            report_day=20 - i,
            hours_today=1,
            hours_total=5,
            task_description='Study',
            discipline_score=5,
            discipline_max=10,
        )
    assert get_user_streak(learner_user) == 1  # Only today counts


@pytest.mark.django_db
def test_streak_zero_for_no_reports(learner_user):
    assert get_user_streak(learner_user) == 0


# ─── Test 4: Mentor Dashboard Access ───────────────────────────────────────

@pytest.mark.django_db
def test_mentor_can_access_dashboard(client, mentor_user):
    client.force_login(mentor_user)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_learner_cannot_access_dashboard(client, learner_user):
    client.force_login(learner_user)
    response = client.get(reverse('dashboard'))
    assert response.status_code == 403
