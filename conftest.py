import pytest
from pytest_factoryboy import register
from tests.factories import ProfileFactory, UserFactory

register(ProfileFactory)
register(UserFactory)

# Create the fixtures


@pytest.fixture
def base_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_superuser=True, is_staff=True)
    return new_user


@pytest.fixture
def profile(db, profile_factory):
    new_profile = profile_factory.create()
    return new_profile
