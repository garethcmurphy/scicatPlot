#!/usr/bin/env python3
"""get api"""
import os


class GetApi:
    """get api"""

    def __init__(self):
        # self.api = "http://127.0.0.1:3000/"
        self.api = "https://scitest.esss.lu.se/"
        # self.api = "https://scicat.esss.se/"

    def get(self):
        """get api"""
        return self.api


def main():
    """main"""
    vis = GetApi()
    print(vis.get())


if __name__ == "__main__":
    main()
