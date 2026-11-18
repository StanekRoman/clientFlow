
import pytest

from django.core.exceptions import ValidationError

from accounts.models import User
from customers.models import Customer
from projects.models import Project, ProjectMember, Task


@pytest.mark.django_db
def test_task_rejects_assignee_from_another_project():
    customer = Customer.objects.create(name="Acme Studio")

    project_a = Project.objects.create(
        customer=customer,
        name="Project A",
    )
    project_b = Project.objects.create(
        customer=customer,
        name="Project B",
    )

    developer = User.objects.create_user(
        email="developer@example.com",
        password="TestPassword123!",
    )

    membership = ProjectMember.objects.create(
        project=project_b,
        user=developer,
    )

    task = Task(
        project=project_a,
        title="Implement API",
        assignee=membership,
    )

    with pytest.raises(ValidationError) as exc_info:
        task.full_clean()

    assert "assignee" in exc_info.value.message_dict


@pytest.mark.django_db
def test_task_accepts_assignee_from_same_project():
    customer = Customer.objects.create(name="Acme Studio")

    project = Project.objects.create(
        customer=customer,
        name="Project A",
    )

    developer = User.objects.create_user(
        email="developer@example.com",
        password="TestPassword123!",
    )

    membership = ProjectMember.objects.create(
        project=project,
        user=developer,
    )

    task = Task(
        project=project,
        title="Implement API",
        assignee=membership,
    )

    task.full_clean()
