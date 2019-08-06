#!/usr/bin/env python3
"""attach image to scicat"""
import platform
import urllib

import base64
import requests
import keyring


class ScicatAttach:
    """attach image to scicat"""
    url_base = "https://scicatapi.esss.dk"
    api = "/api/v3/"
    url_fragment = "Datasets"
    thumbnail = ""
    file = "data/nicos_00000332.hdf"
    options = {}
    header = ""

    def __init__(self):
        self.token = ""

    def get_url(self):
        """get URL"""
        uri = self.url_base + self.api + self.url_fragment + "?access_token=" + self.token
        print(uri)
        return uri

    def get_access_token(self):
        """get access token"""
        username = "ingestor"
        if platform.system() == 'Darwin':
            password = keyring.get_password('scicat', username)
        else:
            with open("config.json") as json_file:
                data = json.load(json_file)
                username = data["username"];
                password = data["password"];

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
        file = "phs.png"
        self.header = "data:image/png;base64,"
        with open(file, 'rb') as image_file:
            data = image_file.read()
            image_bytes = base64.b64encode(data)
            image_str = image_bytes.decode('UTF-8')
            self.thumbnail = self.header + image_str
        return self.thumbnail

    def create_payload(self, pid, file):
        """create payload"""
        encode = self.base64encode(file)
        assert isinstance(encode, str)
        payload = {
            "thumbnail": encode,
            "caption": "pulse height spectrum",
            "datasetId": pid
        }
        # print(payload)
        return payload

    def attach(self, pid, file):
        self.get_access_token()
        """attach image to scicat"""
        quote_pid = urllib.parse.quote_plus(pid)
        post_url = self.url_base + self.api + \
            "Datasets/" + quote_pid + "/datasetattachments" + \
            "?access_token=" + self.token
        payload = self.create_payload(pid, file)
        print("attach", post_url)
        response = requests.post(post_url,  json=payload)
        print(response.json())


def main():
    """attach image to scicat"""
    attach = ScicatAttach()
    pid = "feji"
    file = "phs.png"
    attach.base64encode(file)
    attach.attach(pid, file)


if __name__ == "__main__":
    main()
