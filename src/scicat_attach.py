#!/usr/bin/env python3
"""attach image to scicat"""
import platform

import base64
import requests
import keyring


class ScicatAttach:
    """attach image to scicat"""
    url_base = "https://scicatapi.esss.dk"
    api = "/api/v3/"
    url_fragment = "Datasets"
    thumbnail = ""
    file = "data/nicos_0000322.hdf"
    options = {}

    def __init__(self):
        self.token = ""

    def get_url(self):
        """get URL"""
        uri = self.url_base + self.api + self.url_fragment + "?access_token=" + self.token
        print(uri)
        return uri

    def get_access_token(self):
        """get access token"""
        if platform.system() == 'Darwin':
            username = "ingestor"
            password = keyring.get_password('scicat', username)
        else:
            pass

        token = ""

        login_url = self.url_base + self.api + "/Users/login"
        config = {
            "username": username,
            "password": password
        }
        response = requests.post(login_url, data=config)
        print(response.json())
        token = response.json()
        self.token = token["id"]

        return token["id"]

    def login(self):
        """login to scicat"""
        self.get_access_token()
        print("login")

    def base64encode(self, file):
        """base 64 encode a file"""
        with open(self.file, "rb"):
            self.thumbnail = base64.b64encode(file)
        return self.thumbnail

    def create_payload(self, pid):
        """create payload"""
        payload = {
            "thumbnail": "retrieve",
            "caption": "pulse height spectrum",
            "datasetId": pid
        }
        return payload

    def attach(self, pid):
        """attach image to scicat"""
        post_url = self.url_base + self.api + "Datasets/" + pid + "/datasetattachments"
        print("attach", post_url)


def main():
    """attach image to scicat"""
    attach = ScicatAttach()
    attach.get_access_token()
    pid = "feji"
    attach.attach(pid)


if __name__ == "__main__":
    main()
