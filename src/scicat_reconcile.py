#!/usr/bin/env python3
"""search scicat"""
import os

from scicat_search import ScicatSearch
from data_dir import DataDir


class ScicatReconcile:
    """scicat search"""
    data_directory = "./data/"
    missing = []
    locationUnknown = []
    file_path = ""

    def walk_tree(self):
        """walk tree find files and query scicat"""
        data = DataDir()
        self.data_directory = data.directory_name
        files = os.listdir(self.data_directory)
        for file in files:
            tag = file.strip(".hdf")
            print(tag)
            search = ScicatSearch()
            result = search.search_scicat(tag, 1)
            # print(result)
            if len(result) > 0:
                print(result[0]["sourceFolder"])
                self.file_path = result[0]["sourceFolder"]
                file_exists = self.check_file_path()
                if file_exists != True:
                    self.locationUnknown.append(file)
            else:
                self.missing.append(file)

    def check_file_path(self):
        """check file exists"""
        file_exists = False
        if os.path.isfile(self.file_path):
            file_exists = True
        return file_exists


    def report_missing(self):
        """report missing"""
        print("missing files")
        for file in self.missing:
            print(file)


def main():
    """main"""
    reconcile = ScicatReconcile()
    reconcile.walk_tree()
    reconcile.report_missing()


if __name__ == "__main__":
    main()
