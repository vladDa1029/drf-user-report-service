import pytest
from django.db.models import QuerySet
from model_bakery import baker

from apps.users.filters import UserFilter
from apps.users.models import User, UserStatus


@pytest.mark.parametrize("status,count", [(UserStatus.ACTIVE, 5), (UserStatus.BANNED, 7)])
@pytest.mark.django_db
def test_filter_status(status, count) -> None:
    """Check qweryset|search by 'status'."""
    baker.make("users.User", status=status, _quantity=count)
    baker.make("users.User", status=UserStatus.INACTIVE, _quantity=count)
    qs = UserFilter(data={"status": status}).qs
    assert qs.count() == count
    assert all(u.status == status.value for u in qs)


@pytest.mark.parametrize("status,count", [(UserStatus.ACTIVE, 7), (UserStatus.BANNED, 11)])
@pytest.mark.django_db
def test_filter_ordering_status(status, count) -> None:
    """Check sort order by fields 'status'."""
    baker.make("users.User", status=status, _quantity=count)
    qs = UserFilter(data={"ordering": "status"}).qs
    assert all(qs[i].id < qs[i + 1].id for i in range(qs.count() - 1))


@pytest.mark.parametrize(
    "first_name,last_name,name,expected",
    [
        ("Ivan", "Petrov", "Ivan", 1),  # совпадение по имени
        ("Ivan", "Petrov", "Petrov", 1),  # совпадение по фамилии → проверяет OR
        ("Alexander", "Ivanov", "lex", 1),  # подстрока в имени (icontains)
        ("Maria", "Sidorova", "dorov", 1),  # подстрока в фамилии
        ("Elena", "Kuznetsova", "elena", 1),  # другой регистр → проверяет icontains
        ("Sergey", "Volkov", "Smirnov", 0),  # ничего не совпало → негативный кейс
    ],
)
@pytest.mark.django_db
def test_search_name(first_name: str, last_name: str, name: str, expected: int) -> None:
    """Check search by fields 'first name' or 'last name'.
    Be careful with registers
    """

    baker.make("users.User", first_name=first_name, last_name=last_name)
    qs: QuerySet[User] = UserFilter(data={"name": name}).qs
    assert qs.count() == expected
