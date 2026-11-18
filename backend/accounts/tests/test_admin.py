import pytest

from django.urls import reverse

from ..models import User


@pytest.mark.django_db
def test_user_admin_add_page(admin_client):
    url = reverse("admin:accounts_user_add")

    response = admin_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_admin_creates_user(admin_client):
    url = reverse("admin:accounts_user_add")

    response = admin_client.post(
        url,
        {
            "email": "developer@example.com",
            "usable_password": "true",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
            "_save": "Save",
        },
    )

    assert response.status_code == 302

    user = User.objects.get(email="developer@example.com")

    assert user.check_password("TestPassword123!")
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_user_admin_updates_user(admin_client):
    user = User.objects.create_user(
        email="developer@example.com",
        password="TestPassword123!",
    )

    url = reverse("admin:accounts_user_change", args=[user.pk])

    response = admin_client.post(
        url,
        {
            "email": user.email,
            "password": user.password,
            "first_name": "Roman",
            "last_name": "Developer",
            "is_active": "on",
            "_save": "Save",
        },
    )
    assert response.status_code == 302

    user.refresh_from_db()
    assert user.first_name == "Roman"
    assert user.last_name == "Developer"
    assert user.check_password("TestPassword123!")


@pytest.mark.django_db
def test_regular_user_cannot_access_admin(client):
    user = User.objects.create_user(
        email="developer@example.com",
        password="TestPassword123!",
    )
    client.force_login(user)

    response = client.get(reverse("admin:accounts_user_changelist"))

    assert response.status_code == 302
