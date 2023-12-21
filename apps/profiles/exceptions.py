from rest_framework.exceptions import APIException


class ProfileDoesNotExist(Exception):
    """Raised when a profile is not found."""

    status_code = 404
    default_detail = "Profile not found."
    default_code = "profile_not_found"


class NotYourProfileError(Exception):
    """Raised when a user tries to access a profile that is not theirs."""

    status_code = 403
    default_detail = "You do not have permission to access this profile."
    default_code = "not_your_profile"


class ProfileCreationError(Exception):
    """Raised when there is an error creating a profile."""

    status_code = 400


class ProfileUpdateError(Exception):
    """Raised when there is an error updating a profile."""


class ProfileDeletionError(Exception):
    """Raised when there is an error deleting a profile."""


# Add more custom exceptions as needed...
