# CFXS License Header Generator
# Copyright (C) 2021 | CFXS / Rihards Veips <https://github.com/CFXS/CFXS-License-Header-Generator>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import glob
import linecache
import argparse

usage = "Args: [param_RootPath, param_LicenseFile]"
parser = argparse.ArgumentParser(usage=usage)
parser.add_argument("RootPath", type=str)
parser.add_argument("LicenseFile", type=str)
args = parser.parse_args()

param_RootPath = args.RootPath.replace('\\', '/')
param_LicenseFile = args.LicenseFile.replace('\\', '/')

param_HeaderID = linecache.getline(param_LicenseFile, 1)[:-1]
param_Title = linecache.getline(param_LicenseFile, 2)[:-1]
param_Copyright = linecache.getline(param_LicenseFile, 3)[:-1]

print(f"[UpdateHeaders_GPLv3]\n \
    Root:       {param_RootPath}\n \
    ID:         {param_HeaderID}\n \
    Title:      {param_Title}\n \
    Copyright:  {param_Copyright}")

licenseTemplate = open(os.path.abspath(os.path.dirname(
    __file__)).replace('\\', '/') + "/GPLv3.lic").read()
licenseString = licenseTemplate.replace(
    "${TITLE}", param_Title).replace("${COPYRIGHT}", param_Copyright)


def get_files_recursive(path, filters, identifier):
    files = []
    for x in os.walk(path):
        for filt in filters:
            for filePath in glob.glob(os.path.join(x[0], filt)):
                firstLine = open(filePath).read()
                if firstLine.find(identifier) != -1:
                    files.append(filePath.replace('\\', '/'))
    return files


files = get_files_recursive(
    param_RootPath, ("*.c", "*.cpp", "*.h", "*.hpp"), param_HeaderID)

for filePath in files:
    with open(filePath, "r+") as file:
        fileContent = file.read()
        fileContentOrig = fileContent
        id_offset = fileContent.find(param_HeaderID)
        fileContent = licenseString + '\n' + fileContent[id_offset:]
        if(fileContent != fileContentOrig):
            file.seek(0)
            file.write(fileContent)
            file.truncate()
            file.close()
            print(f"Updated {filePath[len(param_RootPath):]}")
print("> Done")
