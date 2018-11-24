import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    """
    Same as django.contrib.auth.validators.UnicodeUsernameValidator but
    without @.
    """

    regex = r'^[\w.+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and ./+/-/_ characters.'
    )
    flags = re.UNICODE
