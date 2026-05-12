import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def mentor_user(db):
    return User.objects.create_user(
        username='mentor1',
        password='testpass123',
        role='mentor'
    )


@pytest.fixture
def learner_user(db):
    return User.objects.create_user(
        username='learner1',
        password='testpass123',
        role='learner'
    )
