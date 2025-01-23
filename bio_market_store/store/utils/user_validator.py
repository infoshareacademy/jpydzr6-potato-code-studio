import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UserValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters."),
                code="password_too_short",
            )

        if not re.search(r"[a-z]", password):
            raise ValidationError(
                _("This password must contain at least one lowercase letter."),
                code="password_no_lower",
            )
        if not re.search(r"[A-z]", password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code="password_no_upper",
            )

        if not re.search(r"[0-9]", password):
            raise ValidationError(
                _("This password must contain at least one number."),
                code="password_no_digit",
            )

        if not re.search(r"[\W_]", password):
            raise ValidationError(
                _("This password must contain at least one special character."),
                code="password_no_special_char",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, including one lowercase letter, "
            "one uppercase letter, one digit, and one special character."
        )
