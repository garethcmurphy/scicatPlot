#!/usr/bin/env python3
"""search scicat"""
import os
import json
import urllib

import requests


class ScicatSearch:
    """scicat search"""
    base_url = "https://scicatapi.esss.dk"
    api_url = base_url + "/api/v3/"
    dataset_url = api_url + "Datasets/"

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


def main():
    """main"""
    search = ScicatSearch()
    response = search.search_scicat("nicos_00000332", 1)
    if len(reponse) == 0:
        print("no entries found in scicat")
        return 0
    result = response.pop()
    print(result["pid"])
    print(result["pid"])
    path = result["sourceFolder"]
    oldname = result["scientificMetadata"]["file_name"]
    basename = os.path.basename(oldname)
    fullpath = os.path.join(path, basename)
    print(fullpath)


if __name__ == "__main__":
    main()
