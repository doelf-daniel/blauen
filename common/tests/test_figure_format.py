from common.figure_format import sep


def test_sep_one_trailing_zero():
    value = 1.0
    act = sep(value, num_of_decimals=3, thou="'", dec=".")
    assert '1.000' == act


def test_sep_one_trailing_zero_1():
    value = 1.
    act = sep(value, num_of_decimals=3, thou="'", dec=".")
    assert '1.000' == act


def test_sep_one_trailing_zero_2():
    value = 1.23
    act = sep(value, num_of_decimals=3, thou="'", dec=".")
    assert '1.230' == act
