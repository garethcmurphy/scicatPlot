#!/usr/bin/env python3
"""plot nexus file """
import h5py


class ScicatMet:
    """get metadata from nexus file """

    def __init__(self):
        self.file_name = "data/nicos_00000332.hdf"
        self.file_name = "data/nicos_00000490.hdf"
        print("test")

    def set_filename(self, file_name):
        """setter for filename"""
        self.file_name = file_name

    def get_dataset(self, file, path):
        """get dataset from file"""
        val = ""
        if path in file:
            val = file[path][()]
            print(path, val)
        else:
            print("path missing")
            return 0
        return val

    def get_metadata(self):
        """read nexus file"""
        if not h5py.is_hdf5(self.file_name):
            print("Invalid file", self.file_name)
            return 0
        file = h5py.File(self.file_name, "r")
        event_path = "/entry/monitor_1/events/event_id"
        if event_path in file:
            pass
        else:
            print("path missing")
            return 0

        path = "/entry/title"
        title = self.get_dataset(file, path)
        path = "/entry/sample/description"
        sample_description = self.get_dataset(file, path)
        path = "/entry/start_time"
        start_time = self.get_dataset(file, path)
        path = "/entry/instrument/tilting_angle_2/velocity/value"
        tilting_angle_2 = self.get_dataset(file, path)


def main():
    """main"""
    sci = ScicatMet()
    sci.get_metadata()


if __name__ == "__main__":
    main()
