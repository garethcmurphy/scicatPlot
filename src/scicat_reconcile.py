#!/usr/bin/env python3
"""search scicat"""
import os
import json
import urllib

import requests


class ScicatReconcile:
    """scicat search"""
    base_url = "https://scicatapi.esss.dk"
    api_url = base_url + "/api/v3/"
    dataset_url = api_url + "Datasets/"
    data_directory = "./data/"

    def search_scicat(self, text, max_number_results):
        """search scicat"""
        fields = {'text': text}
        limit = {'limit': max_number_results, 'order': "creationTime:desc"}
        fields_encode = urllib.parse.quote(json.dumps(fields))
        limit_encode = urllib.parse.quote(json.dumps(limit))
        dataset_url = self.dataset_url + "anonymousquery?fields=" + \
            fields_encode+"&limits="+limit_encode
        response = requests.get(dataset_url).json()
        print(len(response), "result found!")
        return response

    def walk_tree(self):
        """walk tree find files and query scicat"""
        files = os.listdir(self.data_directory)
        print(files)

    def report_missing(self):
        """report missing"""


def main():
    """main"""
    reconcile = ScicatReconcile()
    reconcile.walk_tree()


if __name__ == "__main__":
    main()
