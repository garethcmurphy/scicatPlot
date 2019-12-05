#!/usr/bin/env python3
"""plot nexus file """
import os
import pprint
import glob
import socket
import urllib
import urllib.parse

import h5py
import numpy as np

import requests

from scicat_login import Login
from scicat_search import ScicatSearch
from get_api import GetApi
from scicat_orig import SciCatOrig


class ScicatMet:
    """get metadata from nexus file """
    files = []
    token = ""
    api = ""
    url = ""
    pid = ""

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

    def get_size(self):
        """get file size"""
        stats = os.stat(self.file_name)
        return stats.st_size

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
        maximum = np.max(array)
        mean = np.mean(array)
        minimum = np.min(array)
        return maximum, mean, minimum

    def look_for_arrays(self):
        """check which arrays are populated"""

    def get_event_num(self, tag, path):
        """get event num"""
        val = ""
        if path in self.file:
            val = self.file[path][()]
            count_events = len(val)
            self.metadata_dict[tag] = {
                "type": "number", "value": count_events, "unit": ""}
        else:
            print("path missing", path)
            return 0
        return 0

    def get_elapsed_time(self, tag, path):
        """get dataset from file"""
        val = ""
        if path in self.file:
            val = self.file[path][()]
            print(type(val))
            print(len(val))
            if val.size > 0:
                return 0
            beg = val[0]/1e9
            end = val[-1]/1e9
            print(beg, end)
            diff = end - beg
            print(diff)
            self.metadata_dict[tag] = {"type": "measurement", "value": str(diff), "unit": "s"}
            return diff
        return 0

    def get_array(self, tag, path):
        """get dataset from file"""
        val = ""
        if path in self.file:
            val = self.file[path][()]
            # self.metadata_dict[base] = val[:]
            print(type(val))
            print(len(val))
            if val.size > 0:
                max_arr, mean_arr, min_arr = self.get_ave_max_min(val)
                print(max_arr, mean_arr, min_arr)
                self.metadata_dict[tag +
                                   "_max"] = {"type": "measurement", "value": max_arr, "unit": ""}
                self.metadata_dict[tag +
                                   "_mean"] = {"type": "measurement", "value": mean_arr, "unit": ""}
                self.metadata_dict[tag +
                                   "_min"] = {"type": "measurement", "value": min_arr, "unit": ""}

            print(path)
        else:
            print("path missing", path)
            return 0
        return 0

    def get_metadata(self):
        """read nexus file"""
        stats = os.stat(self.file_name)
        if stats.st_size < 6048:
            print("Invalid file", self.file_name)
            print("file size", stats.st_size)
            return 0

        if not h5py.is_hdf5(self.file_name):
            print("Invalid file", self.file_name)
            return 0
        try:
            with h5py.File(self.file_name, "r", libver="latest", swmr=True) as file:
                pass
                # print(file["/entry/title"])
        except OSError as err:
            print("OS error: {0}".format(err))
            print("Error reading hdf5 file")
            return
        self.file = h5py.File(self.file_name, "r", swmr=True)

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
        path = "/entry/sample/temperature5/value"
        self.get_array("sample_temperature5", path)
        path = "/entry/instrument/detector_1/raw_event_data/event_id"
        self.get_event_num("count_events", path)
        path = "/entry/monitor_1/events/event_time_zero"
        self.get_elapsed_time("elapsed_time", path)

        scratch = self.file_name.split("_").pop()
        run_number = int(scratch[0:-4])

        self.metadata_dict["runNumber"] = self.set_metadata(
            scicat_type="number", value=run_number, unit="")

        # for i in range(1, 9):
        #    path = "/entry/instrument/chopper_"+str(i)+"/radius"
        #    self.get_dataset("chopper_"+str(i)+"_radius", path)
        #    path = "/entry/instrument/chopper_"+str(i)+"/name"
        #    self.get_dataset("chopper_"+str(i)+"_name", path)

        print("\n\n")
        printer = pprint.PrettyPrinter(indent=4)
        printer.pprint(self.metadata_dict)

    def post_metadata(self):
        """post to scicat"""
        search = ScicatSearch()
        fragment = os.path.basename(self.file_name).replace(".hdf", "")
        print(fragment)
        response = search.search_scicat(fragment, 1)
        # print(response)
        result = response[0]
        self.pid = result["pid"]
        size = self.get_size()
        if result["size"] == 0:
            result["size"] = size
        updated_metadata = result
        updated_metadata["scientificMetadata"] = self.metadata_dict
        # print(updated_metadata)
        pid_encode = urllib.parse.quote_plus(self.pid)
        self.create_url(pid_encode)
        response = requests.post(self.url, json=updated_metadata)
        # print(response.json())

    def create_url(self, pid):
        """create url"""
        apix = GetApi()
        self.api = apix.api
        assert len(self.token) == 64
        #self.url = self.api + "Datasets/updateScientificMetadata?access_token="+self.token
        self.url = self.api + "Datasets/" + pid + \
            "/replace" + "?access_token="+self.token
        print(self.url)

    def get_files(self, my_dir):
        """get files """
        self.files = glob.glob(my_dir + '/**.*', recursive=True)
        print("getting files")
        self.files.sort()
        print(self.files)
        return self.files

    def loop(self):
        """loop files"""
        login = Login()
        self.token = login.get_access_token()
        host_name = socket.gethostname()
        directory_name = "./data"
        if host_name == "CI0020036":
            directory_name = "./data"
        else:
            directory_name = "/nfs/groups/beamlines/v20/YC7SZ5"
        self.get_files(directory_name)
        orig = SciCatOrig()
        for file in self.files:

            stats = os.stat(file)
            if stats.st_size > 7000:
                self.file_name = file
                print(file)
                self.get_metadata()
                self.post_metadata()
                #orig.create_orig(file=self.file_name, pid=self.pid)


def main():
    """main"""
    sci = ScicatMet()
    sci.loop()


if __name__ == "__main__":
    main()
