from os import walk, remove
from os.path import join
import logging

logging.basicConfig(level=logging.DEBUG, filename='log.log')

filer = []

for dirpath, dirnames, filenames in walk(r'Q:\CPK\Byggesag\ejendomme'):
    for file in filenames:
        if file.endswith('.xls') or file.endswith('.xlsx'):
            filepath = join(dirpath, file)
            try:
                remove(filepath)
                print(f'{filepath} SLETTET')
                logging.info(f'{filepath} slettet')
            except PermissionError:
                print(f'PERMISSIONERROR i {filepath}')
                logging.debug(f'PermissionError i {filepath}')
