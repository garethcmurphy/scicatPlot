#!/usr/bin/env python3
"""visualise catalogue"""
import os

from scicat_search import ScicatSearch
from scicat_attach import ScicatAttach
from scicat_plot import ScicatPlot


class ScicatVis:
    """visualise catalogue"""

    def run_vis(self, tag):
        os.remove("phs.png")
        search = ScicatSearch()
        response = search.search_scicat(tag, 1)
        result = response.pop()
        file_name = result["scientificMetadata"]["file_name"]
        pid = result["pid"]
        basename = os.path.basename(file_name)

        plot = ScicatPlot()
        plot.set_filename("data/"+basename)
        plot.plot()
        attach = ScicatAttach()
        file = "phs.png"
        attach.attach(pid, file)

    def loop(self):
        for i in range(480,490)
            tag = "nicos_00000"+i.zfill(3)
            self.run_vis(tag)

def main():
    vis = ScicatVis()
    tag="nicos_00000490"
    vis.run_vis()


if __name__ == "__main__":
    main()
