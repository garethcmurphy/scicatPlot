#!/usr/bin/env python3
"""search scicat"""
import os
import json
import urllib

import requests
from get_api import GetApi


class ScicatSearch:
    """scicat search"""
    base_url = ""

    def __init__(self):
        api = GetApi()
        self.base_url = api.get()
        self.api_url = self.base_url + "api/v3/"
        self.dataset_url = self.api_url + "Datasets/"

    def search_scicat(self, text, max_number_results):
        """search scicat"""
        fields = {'text': text}
        limit = {'limit': max_number_results, 'order': "creationTime:desc"}
        fields_encode = urllib.parse.quote(json.dumps(fields))
        limit_encode = urllib.parse.quote(json.dumps(limit))
        dataset_url = self.dataset_url + "anonymousquery?fields=" + \
            fields_encode+"&limits="+limit_encode
        # print(dataset_url)
        response = requests.get(dataset_url).json()
        print(len(response), "result found!")
        return response


def main():
    """main"""
    search = ScicatSearch()
    response = search.search_scicat("nicos_00000490", 1)
    print("response length", len(response))
    if not response:
        print("no entries found in scicat")
        return 0
    result = response[0]
    print(result["pid"])
    path = result["sourceFolder"]
    oldname = result["scientificMetadata"]["file_name"]
    basename = os.path.basename(oldname)
    fullpath = os.path.join(path, basename)
    print(fullpath)


if __name__ == "__main__":
    main()
