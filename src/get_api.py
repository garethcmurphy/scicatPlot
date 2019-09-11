#!/usr/bin/env python3
"""get api"""


class GetApi:
    """get api"""

    def __init__(self):
        self.api = "https://scicat.esss.se/"
        self.api = "http://localhost:3000/"

    def get(self):
        """get api"""
        return self.api


def main():
    """main"""
    vis = GetApi()
    print(vis.get())


if __name__ == "__main__":
    main()
