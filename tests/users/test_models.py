import pytest


def test_user_str(base_user):
    """Test the custom user model string representation"""
    assert str(base_user) == base_user.username


def test_user_short_name(base_user):
    """Test the custom user model short name"""
    assert base_user.get_short_name() == f"{base_user.username}"


def test_user_full_name(base_user):
    """Test the custom user model full name"""
    full_name = f"{base_user.first_name.title()} {base_user.last_name.title()}"
    assert base_user.get_fullname == full_name


# Testing the user manager


def test_base_user_email_is_normalized(base_user):
    """Test the email for a new user is normalized"""
    # This is the email we are testing should be converted to lowercase
    email = base_user.email
    assert base_user.email == email.lower()


def test_super_user_email_is_normalized(super_user):
    """Test the email for a new superuser is normalized"""
    email = super_user.email
    assert super_user.email == email.lower()


def test_superuser_is_staff(user_factory):
    """Test the is_staff for a new superuser is True"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(err.value) == "Superuser must have is_staff=True."


def test_superuser_is_not_superuser(user_factory):
    """Test the is_superuser for a new superuser is True"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == "Superuser must have is_superuser=True."


def test_create_user_with_no_email(user_factory):
    """Test creating a user with no email raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(
            email=None,
        )
    assert str(err.value) == "The Email must be set"


def test_create_user_with_no_username(user_factory):
    """Test creating a user with no username raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "User must have a username"


def test_create_user_with_no_password(user_factory):
    """Test creating a user with no password raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None)
    assert str(err.value) == "User must have a password"


def test_create_user_with_no_first_name(user_factory):
    """Test creating a user with no first name raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "User must have a first name"


def test_create_user_with_no_last_name(user_factory):
    """Test creating a user with no last name raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "User must have a last name"


def test_create_superuser_with_no_email(user_factory):
    """Test creating a user with no email raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Super User must provide email address!"


def test_create_superuser_with_no_password(user_factory):
    """Test creating a user with no password raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None, is_staff=True, is_superuser=True)
    assert str(err.value) == "Super user must have a password"


from django.core.exceptions import ValidationError


def test_create_user_email_incorrect_format(user_factory):
    """Test creating a user with invalid email raises an error"""
    with pytest.raises(ValidationError) as err:
        user_factory.create(email="miclem.com")
    assert str(list(err.value)[0]) == "You must provide a valid email address"
