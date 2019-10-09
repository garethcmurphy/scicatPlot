#!/usr/bin/env python3
"""scicat orig"""
import urllib

import requests
from file_info import FileInfo
from get_api import GetApi
from scicat_login import Login


class SciCatOrig:
    """scicat orig"""
    orig = {}
    uri = ""
    file = ""
    pid = ""

    def create_json(self):
        """create json"""
        file_info = FileInfo()
        file_entry = file_info.get(file=self.file)
        self.orig = {
            "dataFileList": [file_entry],
            "datasetId": self.pid,
            "ownerGroup": "ess",
            "accessGroups": ["loki", "brightness"],
            "size": file_entry["size"]
        }
        print(self.orig)

    def create_uri(self):
        """create uri"""
        get_api = GetApi()
        login = Login()
        token_object = login.get_access_token()
        print("token object", token_object)
        encode_pid = urllib.parse.quote_plus(self.pid)
        api = get_api.api
        print("api", api)
        token = "?access_token="+token_object
        self.uri = api + "Datasets/" + encode_pid + "/origdatablocks" + token
        print(self.uri)

    def post(self):
        """post to scicat"""
        response = requests.post(self.uri, json=self.orig)
        print(response.json())

    def create_orig(self, pid="vjdfk", file="hjkfe"):
        """post to scicat"""
        self.pid = pid
        self.file = file
        self.create_uri()
        self.create_json()
        self.post()


def main():
    """main"""
    orig = SciCatOrig()
    file = "data/nicos_00000764.hdf"
    pid = "20.500.12269/764nicos_00000764.hdf"
    orig.create_orig(file=file, pid=pid)


if __name__ == "__main__":
    main()
