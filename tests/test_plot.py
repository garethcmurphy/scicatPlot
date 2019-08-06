"""test"""
from scicat_plot import ScicatPlot


def test_scicat():
    """test"""
    sci = ScicatPlot()
    assert isinstance(sci.file_name, str)