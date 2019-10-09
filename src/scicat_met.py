#!/usr/bin/env python3
"""plot nexus file """
import os
import pprint
import glob

import h5py

import requests

from scicat_attach import ScicatAttach
from scicat_search import ScicatSearch
from get_api import GetApi


class ScicatMet:
    """get metadata from nexus file """
    files = []

    def __init__(self):
        self.metadata_dict = {}
        self.file_name = "data/nicos_00000332.hdf"
        self.file_name = "data/nicos_00000490.hdf"
        self.file_name = "/nfs/groups/beamlines/v20/DD1F5G/nicos_00000764.hdf"
        self.file_name = "data/nicos_00000764.hdf"
        self.file = ""
        print(self.file_name)

    def set_filename(self, file_name):
        """setter for filename"""
        self.file_name = file_name

    def set_metadata(self, scicat_type, value, unit):
        """set metadata"""
        obj = {"type": scicat_type, "unit": unit, "value": value}
        return obj

    def get_attribute(self, key, path):
        """get dataset from file"""
        val = ""
        if path in self.file:
            obj = self.file[path]
            val = obj.attrs[key]
            self.metadata_dict[key] = self.set_metadata(
                scicat_type="string", unit="", value=val)
            print(path, val)
        else:
            print("path missing", path)
            return 0
        return val

    def get_dataset(self, key, path):
        """get dataset from file"""
        val = ""
        if path in self.file:
            dset = self.file[path]
            unit = ""
            print(dset.attrs)
            scicat_type = "string"
            if "units" in dset.attrs:
                # print(dset.attrs["units"])
                scicat_type = "measurement"
                unit = dset.attrs["units"]
            val = dset[()]
            self.metadata_dict[key] = self.set_metadata(
                scicat_type=scicat_type, unit=unit, value=val)
            print(path, val)
        else:
            print("path missing", path)
            return 0
        return val

    def get_ave_max_min(self, array):
        """get max mean and min"""
        maximum = max(array)
        mean = sum(array)/len(array)
        minimum = min(array)
        return maximum, mean, minimum

    def look_for_arrays(self):
        """check which arrays are populated"""

    def get_array(self, path):
        """get dataset from file"""
        val = ""
        if path in self.file:
            val = self.file[path][()]
            base = os.path.basename(path)
            # self.metadata_dict[base] = val[:]

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
        path = "/entry/sample/chemical_formula"
        self.get_dataset("sample_description", path)
        path = "/entry/sample/name"
        self.get_dataset("sample_name", path)
        path = "/entry/sample/chemical_formula"
        self.get_dataset("chemical_formula", path)
        path = "/entry/start_time"
        self.get_dataset("start_time", path)
        path = "/"
        self.get_attribute("file_name", path)

        scratch = self.file_name.split("_").pop()
        run_number = int(scratch[0:-4])

        # run_number = 3
        self.metadata_dict["runNumber"] = self.set_metadata(scicat_type="number", value=run_number, unit="")

        for i in range(1, 9):
            path = "/entry/instrument/chopper_"+str(i)+"/radius"
            self.get_dataset("chopper_"+str(i)+"_radius", path)
            path = "/entry/instrument/chopper_"+str(i)+"/name"
            self.get_dataset("chopper_"+str(i)+"_name", path)

        #path = "/entry/instrument/tilting_angle_2/velocity/value"
        # self.get_array(path)

        print("\n\n")
        printer = pprint.PrettyPrinter(indent=4)
        printer.pprint(self.metadata_dict)

    def post_metadata(self):
        """post to scicat"""
        search = ScicatSearch()
        fragment = os.path.basename(self.file_name).replace(".hdf", "")
        print(fragment)
        response = search.search_scicat(fragment, 1)
        print(response)
        result = response[0]
        login = ScicatAttach()
        token = login.get_access_token()
        print(token)
        updated_metadata = result
        updated_metadata["scientificMetadata"] = self.metadata_dict
        print(updated_metadata)
        api = GetApi()
        api = api.get()
        assert len(token) == 64
        # token = "Gkbbx3RT2dzCgmuoqUnwQCdhmvGbukAQcI2onZD3K6j6mywXQrnHVdQPGh2Qw18W"
        url = api + "api/v3/Datasets/updateScientificMetadata?access_token="+token
        print(url)
        response = requests.put(url, json=updated_metadata)
        print(response)

    def get_files(self, my_dir):
        """get files """
        self.files = glob.glob(my_dir + '/**.*', recursive=True)
        return self.files

    def loop(self):
        """loop files"""
        directory_name = "./data"
        self.get_files(directory_name)
        for file in self.files:
            self.file_name = file
            print(file)
            self.get_metadata()
            # self.post_metadata()


def main():
    """main"""
    sci = ScicatMet()
    sci.loop()
    # sci.post_metadata()


if __name__ == "__main__":
    main()
