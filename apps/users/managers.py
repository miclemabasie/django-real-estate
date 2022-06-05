from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomBaseUserManager(BaseUserManager):
    def validate_email(self, email):
        try:
            email = validate_email(email)
        except ValidationError:
            raise ValueError("Email must be provided")

    def create_user(
        self, username, first_name, last_name, email, password, **extra_fields
    ):

        if not username:
            raise ValueError(_("Username must be provided"))

        if not first_name:
            raise ValueError(_("First name must be provided"))

        if not last_name:
            raise ValueError(_("Last Name must be provided"))

        if email:
            email = self.normalize_email(email)
            self.validate_email(email)
        else:
            raise ValueError(_("BaseUser: a valid email address is needed"))

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            emial=email,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)
        return user
