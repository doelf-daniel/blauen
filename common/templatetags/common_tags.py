import decimal
import locale

from django import template
from django.conf import settings

from common.figure_format import sep

register = template.Library()
loc = locale.getlocale()  # get current locale


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


@register.filter(name='int_format')
def int_format(value, grouping_size=3, separator=u'\''):
    if isinstance(value, int):
        value = str(value)
        if len(value) <= grouping_size:
            return value
        # say here we have value = '12345' and the default params above
        parts = []
        while value:
            parts.append(value[-grouping_size:])
            value = value[:-grouping_size]
        # now we should have parts = ['345', '12']
        parts.reverse()
        # and the return value should be u'12.345'
        return separator.join(parts)
    else:
        raise InputError(value, "Not an Integer Value!")


@register.filter
def group_separator(number):
    s = '%d' % number
    number_dec = str(number - int(number))
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    # TODO Replace with locale separator  \b.*
    value = s + u'\''.join(reversed(groups))
    return value + number_dec[1:]


@register.filter
def quantize(value, arg=None):
    """
    :param value:
    :param arg:

    Takes a float number (23.456) and uses the
    decimal.quantize to round it to a fixed
    exponent. This allows you to specify the
    exponent precision, along with the
    rounding method.

    Examples (assuming value="7.325"):
    {% value|quantize %} -> 7.33
    {% value|quantize:".01,ru" %} -> 7.33 (this is the same as the default behavior)
    {% value|quantize:".01,rd" %} -> 7.32

    Available rounding options (taken from the decimal module):
    ROUND_CEILING (rc), ROUND_DOWN (rd), ROUND_FLOOR (rf), ROUND_HALF_DOWN (rhd),
    ROUND_HALF_EVEN (rhe), ROUND_HALF_UP (rhu), and ROUND_UP (ru)

    Arguments cannot have spaces in them.

    See the decimal module for more info:
    http://docs.python.org/library/decimal.html
    """
    num = decimal.Decimal(str(value))
    options = ["ru", "rf", "rd", "rhd", "rhe", "rhu"]
    precision = None
    rounding = None
    if arg:
        args = arg.split(",")
        precision = args[0]
        rounding = str(args[1])
    if not precision:
        precision = ".01"
    if not rounding:
        rounding = decimal.ROUND_UP
    if rounding not in options:
        rounding = decimal.ROUND_UP
    if rounding == "ru":
        rounding = decimal.ROUND_UP
    elif rounding == "rf":
        rounding = decimal.ROUND_FLOOR
    elif rounding == "rd":
        rounding = decimal.ROUND_DOWN
    elif rounding == "rhd":
        rounding = decimal.ROUND_HALF_DOWN
    elif rounding == "rhe":
        rounding = decimal.ROUND_HALF_EVEN
    elif rounding == "rhu":
        rounding = decimal.ROUND_HALF_UP
    newnum = num.quantize(decimal.Decimal(precision), rounding=rounding)
    return newnum


@register.filter
def dec_format(number, num_of_decimals=1):
    if number is None or number == '':
        return ''
    elif isinstance(number, float):
        res = sep(number, num_of_decimals, thou="'", dec=".")
        return res
    else:
        return ''


@register.filter
def integer_unformatted(number):
    if number is None:
        return ''
    else:
        return '{:d}'.format(number)


# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
