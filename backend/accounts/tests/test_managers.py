import pytest

from accounts.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="developer@example.com",
        password="TestPassword123!",
    )

    assert user.email == "developer@example.com"
    assert user.check_password("TestPassword123!")
    assert User.objects.filter(email="developer@example.com").exists()


@pytest.mark.django_db
def test_create_user_normalizes_email():
    user = User.objects.create_user(
        email="  Developer@EXAMPLE.COM  ",
        password="TestPassword123!",
    )

    assert user.email == "developer@example.com"


@pytest.mark.django_db
@pytest.mark.parametrize("email", ["", "   ", None])
def test_create_user_without_email(email):
    with pytest.raises(ValueError, match="Email is required"):
        User.objects.create_user(
            email=email,
            password="TestPassword123!",
        )


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        email="admin@example.com",
        password="TestPassword123!",
    )

    assert user.email == "admin@example.com"
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.check_password("TestPassword123!")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_field",
    ["is_staff", "is_superuser"],
)
def test_create_superuser_rejects_invalid_permissions(invalid_field):
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="admin@example.com",
            password="TestPassword123!",
            **{invalid_field: False},
        )
