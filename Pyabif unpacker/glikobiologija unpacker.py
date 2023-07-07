from zipfile import ZipFile
import os

i=1
path = 'Z:/INSTRUMENTS/TECAN'
entries = os.listdir(path)

def ls_files(dir):
    files = list()
    for item in os.listdir(dir):
        abspath = os.path.join(dir, item)
        try:
            if os.path.isdir(abspath):
                files.append(abspath)
                files = files + ls_files(abspath)
        except FileNotFoundError as err:
            print('invalid directory\n', 'Error: ', err)
    return files

for dir in ls_files(path):
    zips = os.listdir(dir)
    outpath= dir + '/data.1.'
    try:
        for zip in zips:
            if zip.endswith('.fsa.txt.zip'):
                with ZipFile(dir + '/' + zip, 'r') as zippy:
                    zippies = zippy.namelist()
                    for zip in zippies:
                        if zip.endswith('.fsa.data.1.txt'):
                            file = zip
                    zippy.extract(file, outpath)
            else:
                pass
    except FileNotFoundError as err:
            print('invalid directory\n', 'Error: ', err)
