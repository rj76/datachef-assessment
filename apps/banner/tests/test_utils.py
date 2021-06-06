from apps.banner import utils


class TestUtils:
    def test_round_to_quarter(self):
        assert utils.round_to_quarter(1) == 1
        assert utils.round_to_quarter(15) == 2
        assert utils.round_to_quarter(44) == 3
        assert utils.round_to_quarter(46) == 4

    def test_randomize_list(self):
        my_list = [34, 13, 645, 74, 34, 234, 213, 3, 123]
        random = utils.randomize_list(my_list)

        assert ','.join(str(v) for v in my_list) != ','.join(str(v) for v in random)
