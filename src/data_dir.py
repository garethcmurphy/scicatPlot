#!/usr/bin/env python3
"""get api"""
import socket


class DataDir:
    """get api"""
    directory_name = "./data"

    def __init__(self):
        host_name = socket.gethostname()
        if host_name == "CI0020036":
            self.directory_name = "./data"
        else:
            self.directory_name = "/nfs/groups/beamlines/v20/YC7SZ5"


def main():
    """main"""
    DataDir()


if __name__ == "__main__":
    main()
