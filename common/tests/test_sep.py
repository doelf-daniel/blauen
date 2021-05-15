from common.figure_format import sep


def test_sep1():
    s = 12345678.1234
    n = sep(s)
    assert n == "12'345'678.12"


def test_sep2():
    s = -12345678.1234
    n = sep(s, thou="'", dec=".")
    assert n == "-12'345'678.12"


def test_sep3():
    s = 12345678.1450002
    n = sep(s, thou="'", dec=".")
    assert n == "12'345'678.15"


def test_sep4():
    s = -12345678.1450002
    n = sep(s, thou="'", dec=".")
    assert n == "-12'345'678.15"


def test_sep5():
    s = '.'
    n = sep(s, thou="'", dec=".")
    assert n == ''


def test_sep6():
    s = ''
    n = sep(s, thou="'", dec=".")
    assert n == ''
