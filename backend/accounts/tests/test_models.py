import pytest

from django.db import IntegrityError

from accounts.models import User


@pytest.mark.django_db
def test_email_is_case_insensitive_unique():
    User.objects.create_user(
        email="developer@example.com",
        password="TestPassword123!",
    )

    with pytest.raises(IntegrityError):
        User.objects.create(
            email="Developer@Example.com",
        )
