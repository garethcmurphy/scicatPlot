#!/usr/bin/env python3
"""plot nexus file """
import h5py
import numpy as np
import matplotlib.pyplot as plt


class ScicatPlot:
    """plot nexus file """

    def __init__(self):
        self.file_name = "data/nicos_000000332.hdf"
        print("test")

    def set_filename(self, file_name):
        """setter for filename"""
        self.file_name = file_name

    def plot(self):
        """read nexus file"""
        if not h5py.is_hdf5(self.file_name):
            raise ValueError('Not an hdf5 file')
        file = h5py.File(self.file_name, "r")
        event_path = "/entry/monitor_1/events/event_id"
        if event_path in file:
            pass
        else:
            print("path missing")
            return 0

        pulse_height = file[event_path][:]

        mfc = 'cornflowerblue'
        marker = 'o'
        markersize = 3

        _, axp = plt.subplots()

        phs, edgesp = np.histogram(pulse_height, bins=200)
        axp.errorbar(edgesp[:-1], phs, lw=1, yerr=np.sqrt(phs),
                     marker=marker, markersize=markersize, mfc=mfc)
        axp.set_xlabel('Channel')
        axp.set_ylabel('Raw counts')
        axp.set_title('PHS')

        plt.savefig("phs.png")


def main():
    """main"""
    sci = ScicatPlot()
    sci.plot()


if __name__ == "__main__":
    main()
