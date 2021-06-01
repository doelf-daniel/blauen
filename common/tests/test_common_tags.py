from common.templatetags.common_tags import dec_format


def test_dec_format_1():
    number = 1.234
    res = dec_format(number)
    assert '1.2' == res


def test_dec_format_3():
    number = 1.2346789
    res = dec_format(number, num_of_decimals=3)
    assert '1.235' == res


def test_dec_format_3b():
    number = 1.23
    res = dec_format(number, num_of_decimals=3)
    assert '1.230' == res
