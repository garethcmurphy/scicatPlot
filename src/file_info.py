#!/usr/bin/env python3
"""file info"""
import os
import datetime
import hashlib
import pytz


class FileInfo:
    """get file info"""
    file_entry = {}

    def get(self, file):
        """get file info"""
        stat_info = os.stat(file)
        file_size = stat_info.st_size
        experiment_date_time = stat_info.st_ctime
        timestamp = int(experiment_date_time)

        permissions = oct(stat_info.st_mode & 0o777)

        experiment_date_time = str(datetime.datetime.fromtimestamp(
            timestamp, tz=pytz.UTC).isoformat())
        checksum = "string"

        if file_size < 34000000:
            hash_object = hashlib.sha256(open(file, 'rb').read())
            checksum = hash_object.hexdigest()
        self.file_entry = {
            "path": file,
            "size": file_size,
            "time": experiment_date_time,
            "chk": checksum,
            "uid": stat_info.st_uid,
            "gid": stat_info.st_gid,
            "perm": permissions
        }
        return self.file_entry


def main():
    """main"""
    file = FileInfo()
    file.get("data/nicos_00000763.hdf")
    print(file.file_entry)


if __name__ == "__main__":
    main()
