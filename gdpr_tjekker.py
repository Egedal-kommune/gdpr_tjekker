from pathlib import Path
import pandas as pd
import csv
import xlrd

class GdprTjekker:

    def __init__(self, path):
        self.p = Path(path)

    def get_filepaths(self, extension, search_string):
        results = []
        all_files = list(self.p.rglob(f'*.{extension}')) 

        for file in all_files:
            if search_string in file.name.lower():
                results.append(file)
        
        return results

    def tjek_cpr(self, filepath, encoding='utf-8'):
        if Path(filepath).suffix == '.csv' and Path(filepath).name.startswith('~') == False:
            try:
                df = pd.read_csv(filepath, encoding=encoding, sep=None, engine='python')
                cpr_file = False
                for col in df.columns:
                    if self.tjek_column_name(col):
                        cpr_file = True
                        break
                return cpr_file
            except (pd.errors.ParserError, csv.Error) as e:
                return e
        elif Path(filepath).suffix == '.xlsx' and Path(filepath).name.startswith('~') == False:
            try:
                df = pd.read_excel(filepath)
            except (xlrd.biffh.XLRDError, PermissionError, FileNotFoundError) as e:
                return e
            cpr_file = False
            for col in df.columns:
                if self.tjek_column_name(col):
                    cpr_file = True
                    break
            return cpr_file

    def tjek_column_name(self, col_name):
        if 'cpr' in str(col_name).lower():
            return True
        else:
            return False

    def delete_files(self, filepath):
        filepath.unlink()