#!/usr/bin/env python3
"""search scicat"""
import os
import json
import urllib

import requests
from scicat_search import ScicatSearch
from get_api import GetApi


class ScicatReconcile:
    """scicat search"""
    
    data_directory = "./data/"
    missing = []

    def search_scicat(self, text, max_number_results):
        """search scicat"""
        fields = {'text': text}
        limit = {'limit': max_number_results, 'order': "creationTime:desc"}
        fields_encode = urllib.parse.quote(json.dumps(fields))
        limit_encode = urllib.parse.quote(json.dumps(limit))
        api = GetApi()
        api_url = api.get()
        dataset_url = api_url + "/api/v3/Datasets/" + "anonymousquery?fields=" + \
            fields_encode+"&limits="+limit_encode
        response = requests.get(dataset_url).json()
        print(len(response), "result found!")
        return response

    def walk_tree(self):
        """walk tree find files and query scicat"""
        files = os.listdir(self.data_directory)
        for file in files:
            print(file)
            search = ScicatSearch()
            result = search.search_scicat(file, 1)
            print(result)
            print(result[0]["sourceFolder"])

    def report_missing(self):
        for file in self.missing:
            print(file)
        """report missing"""


def main():
    """main"""
    reconcile = ScicatReconcile()
    reconcile.walk_tree()


if __name__ == "__main__":
    main()
