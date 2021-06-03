from apps.banner import utils


def test_round_to_quarter():
    assert utils.round_to_quarter(1) == 1
    assert utils.round_to_quarter(15) == 2
    assert utils.round_to_quarter(44) == 3
    assert utils.round_to_quarter(46) == 4
