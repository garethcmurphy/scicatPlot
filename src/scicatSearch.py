#!/usr/bin/env python3
import os
import requests
import json
import urllib


def search_scicat(text, max_number_results):
    fields = {'text': text}
    limit = {'limit': max_number_results, 'order': "creationTime:desc"}
    fields_encode = urllib.parse.quote(json.dumps(fields))
    limit_encode = urllib.parse.quote(json.dumps(limit))
    dataset_url = "https://scicatapi.esss.dk/api/v3/Datasets/anonymousquery?fields=" + \
        fields_encode+"&limits="+limit_encode
    r = requests.get(dataset_url).json()
    print(len(r), "result found!")
    return r


if __name__ == "__main__":
    r = search_scicat("nicos_00000490", 1)
    result = r.pop()
    print(result["pid"])
    print(result["pid"])
    path = result["sourceFolder"]
    oldname = result["scientificMetadata"]["file_name"]
    basename = os.path.basename(oldname)
    fullpath = os.path.join(path , basename)
    print(fullpath)
