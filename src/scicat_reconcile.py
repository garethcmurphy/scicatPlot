#!/usr/bin/env python3
"""search scicat"""
import os

from scicat_search import ScicatSearch


class ScicatReconcile:
    """scicat search"""
    data_directory = "./data/"
    missing = []

    def walk_tree(self):
        """walk tree find files and query scicat"""
        files = os.listdir(self.data_directory)
        for file in files:
            tag = file.strip(".hdf")
            print(tag)
            search = ScicatSearch()
            result = search.search_scicat(tag, 1)
            # print(result)
            if len(result) > 0:
                print(result[0]["sourceFolder"])
            else:
                self.missing.append(file)

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
