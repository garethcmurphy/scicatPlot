"""attach image to scicat"""
import requests
import keyring


class ScicatAttach:
    """attach image to scicat"""
    url_base = "https://scicatapi.esss.dk"
    api = "/api/v3/"
    url_fragment = "Datasets"
    options = {}

    def __init__(self):
        self.token = ""

    def login(self):
        """login to scicat"""
        print("login")

    def attach(self):
        """attach image to scicat"""
        print("attach")


def main():
    """attach image to scicat"""
    ScicatAttach()


if __name__ == "__main__":
    main()
