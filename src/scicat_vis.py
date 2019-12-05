#!/usr/bin/env python3
"""visualise catalogue"""
import os
import socket

import visens
import h5py


from scicat_search import ScicatSearch
from scicat_attach import ScicatAttach


class ScicatVis:
    """visualise catalogue"""

    def run_vis(self, tag):
        """add plot to data catalogue"""
        try:
            os.remove("phs.png")
        except OSError:
            print("no existing plot file")
        search = ScicatSearch()
        response = search.search_scicat(tag, 1)
        if not response:
            print("no results found, continuing")
            return 0
        result = response[0]
        file_name = result["scientificMetadata"]["file_name"]["value"]
        print(file_name)
        pid = result["pid"]
        print(pid)
        basename = os.path.basename(file_name)

        path = result["sourceFolder"]
        hostname = socket.gethostname()
        if hostname == "CI0020036":
            path = "data/"
        file_path = os.path.join(path, basename)
        print(file_path)
        try:
            with h5py.File(file_path, "r", libver="latest", swmr=True) as file:
                pass
                #print(file["/entry/title"])
        except OSError as err:
            print("OS error: {0}".format(err))
            print("Error reading hdf5 file")
            return 0
        try:
            visens.preview(file_path, log=True, save="phs.png")
        except TypeError as err:
            print("Type error: {0}".format(err))
            print("Error reading hdf5 file")
            return 0
        except ValueError as err:
            print("Type error: {0}".format(err))
            print("Error reading hdf5 file")
            return 0
        attach = ScicatAttach()
        file = "phs.png"
        attach.attach(pid, file)

    def loop(self):
        """loop around files"""
        for i in range(2457, 2463):

            tag = "nicos_0000"+str(i).zfill(4)
            self.run_vis(tag)


def main():
    """main"""
    vis = ScicatVis()
    vis.loop()


if __name__ == "__main__":
    main()
