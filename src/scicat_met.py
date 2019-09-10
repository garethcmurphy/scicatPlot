#!/usr/bin/env python3
"""plot nexus file """
import os

import h5py
import pprint


class ScicatMet:
    """get metadata from nexus file """

    def __init__(self):
        self.metadata_dict = {}
        self.file_name = "data/nicos_00000332.hdf"
        self.file_name = "data/nicos_00000490.hdf"
        self.file = ""
        print("test")

    def set_filename(self, file_name):
        """setter for filename"""
        self.file_name = file_name

    def get_dataset(self,  key, path):
        """get dataset from file"""
        val = ""
        if path in self.file:
            val = self.file[path][()]
            base = os.path.basename(path)
            self.metadata_dict[key] = val
            print(path, val)
        else:
            print("path missing")
            return 0
        return val

    def get_array(self, path):
        """get dataset from file"""
        val = ""
        if path in self.file:
            val = self.file[path][()]
            base = os.path.basename(path)
            self.metadata_dict[base] = val[:]
            print(path, val)
        else:
            print("path missing", path)
            return 0
        return val

    def get_metadata(self):
        """read nexus file"""
        if not h5py.is_hdf5(self.file_name):
            print("Invalid file", self.file_name)
            return 0
        self.file = h5py.File(self.file_name, "r")

        path = "/entry/title"
        self.get_dataset("title", path)
        path = "/entry/sample/description"
        self.get_dataset("sample_description", path)
        path = "/entry/start_time"
        self.get_dataset("start_time", path)
        path = "/file_name"
        self.get_dataset("start_time", path)

        for i in range(9):
            path = "/entry/instrument/chopper_"+str(i)+"/radius"
            self.get_dataset("chopper_"+str(i)+"_radius", path)

        #path = "/entry/instrument/tilting_angle_2/velocity/value"
        # self.get_array(path)

        print("\n\n")
        printer = pprint.PrettyPrinter(indent=4)
        printer.pprint(self.metadata_dict)


def main():
    """main"""
    sci = ScicatMet()
    sci.get_metadata()


if __name__ == "__main__":
    main()
