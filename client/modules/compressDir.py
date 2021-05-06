import os
import tarfile


class CompressDirectory:

    def __init__(self, fileLocation, fileName):
        self.fileLocation = fileLocation
        self.fileName = fileName
        self.exclude_files = [f"{fileName}/node_modules"]

    def filter_function(self, tarinfo):
        filename = tarinfo.name
        return None if filename in self.exclude_files or os.path.splitext(filename)[1] in self.exclude_files else tarinfo

    def compress(self):
        tar = tarfile.open(f"{self.fileName}.tar.gz", "w:gz")
        tar.add(f"{self.fileLocation}",
                arcname=self.fileName, filter=self.filter_function)
        tar.close()
        print('.tar.gz file is created successfully!')
