"""test"""
from scicat_attach import ScicatAttach


def test_scicat():
    """test"""
    sci = ScicatAttach()
    assert isinstance(sci.url_base, str)


def test_payload():
    """test payload"""
    sci = ScicatAttach()
    payload = sci.create_payload("xyz", "x.png")
    assert "thumbnail" in payload
