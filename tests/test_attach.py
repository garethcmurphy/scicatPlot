"""test"""
from scicat_attach import ScicatAttach


def test_scicat():
    """test"""
    sci = ScicatAttach()
    assert isinstance(sci.url_base, str)