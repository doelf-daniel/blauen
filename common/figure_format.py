import logging
import re

logger = logging.getLogger(__name__)


def sep(s, num_of_decimals=2, thou="'", dec="."):
    """

    :param s:
    :param num_of_decimals:
    :param thou:
    :param dec:
    :return:
    """

    # Regex explanation:
    #
    #     \B      # Assert that we're not at the start of the number
    #     (?=     # Match at a position where it's possible to match...
    #      (?:    #  the following regex:
    #       \d{3} #   3 digits
    #      )+     #  repeated at least once
    #      $      #  until the end of the string
    #     )       # (thereby ensuring a number of digits divisible by 3
    #
    if not s:
        return ''
    if isinstance(s, float) or isinstance(s, int):
        r = round(s, num_of_decimals)
        str1 = str(r)
        integer, decimal = str1.split('.')
        integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)

        if len(decimal) < num_of_decimals:
            for i in range(num_of_decimals - len(decimal)):
                decimal += '0'
        return integer + dec + decimal
    else:
        logger.error("wrong data type, value = {}".format(s))
        # raise TypeError()
        return ''
