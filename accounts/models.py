from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [('learner', 'Learner'), ('mentor', 'Mentor')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='learner')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_mentor(self):
        return self.role == 'mentor'
