"""test"""
from scicat_search import ScicatSearch


def test_scicat():
    """test"""
    sci = ScicatSearch()
    assert isinstance(sci.base_url, str)