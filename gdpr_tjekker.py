from pathlib import Path
import pandas as pd
import csv
import xlrd
from tqdm import tqdm

class GdprTjekker:
    """
    Parameters
    ----------
    path : str
        Stien til den folder, som skal kigges igennem

    extensions : list
        En liste over de filformater, der skal søges efter
    
    search_string : str
        Den tekst, der skal være tilstede i et filnavn (Default ingenting, dvs. der søges efter alle filer)

    Returns
    -------
    GdprTjekker object
    
    """

    def __init__(self, path, extensions, search_string=''):
        self.p = Path(path)
        self.extensions = extensions
        self.search_string = search_string

    def get_filepaths(self, extension):
        """Henter alle filer, der passer til søgekriterierne

        Parameters
        ----------
        extension : str
            Hvilken filekstension skal der kigges efter? csv eller xlsx?

        Returns
        -------
        list
            En liste med alle de filer, der er fundet på den angivne sti
        """
        results = []
        all_files = list(self.p.rglob(f'*.{extension}')) 

        for file in all_files:
            if self.search_string in file.name.lower():
                results.append(file)
        
        return results

    def tjek_cpr(self, filepath, encoding='utf-8'):
        """Tjekker om der er en kolonne, som hedder noget med 'cpr'.

        Parameters
        ----------
        filepath : str
            Stien til den fil, som skal kigges i
        
        encoding : str
            Den encoding, som filerne har (Default er 'utf-8')
        
        Returns
        -------
        bool
            True hvis filen indeholder en kolonne, som hedder noget med 'cpr', ellers False
        """
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
        """Tjekker om navnet på en kolonne indeholder 'cpr'

        Parameters
        ----------
        col_name : str
            Navnet på den kolonne, som skal tjekkes efter

        Returns
        -------
        bool
            True hvis kolonnenavn har 'cpr' i ellers False
        """
        if 'cpr' in str(col_name).lower():
            return True
        else:
            return False

    def delete_files(self, filepath):
        """Sletter en given fil

        Parameters
        ----------
        filepath : str
            Sti til den fil, der skal slettes
        """
        filepath.unlink()
    
    def write_to_xlsx(self, file_encoding):
        """Skriver resultaterne ned i en excelfil

        Parameters
        ----------
        file_encoding : str
            Encoding på de filer, som skal kigges igennem.
        
        Returns
        -------
        En fil med navnet GDPR_TJEK.xlsx, som ligger i roden.
        """
        filer = {key: None for key in self.extensions}

        for filformat in self.extensions:
            cpr_filer = []
            files = self.get_filepaths(filformat)
            for file in tqdm(files):
                if self.tjek_cpr(file, file_encoding):
                    cpr_filer.append(file)
            filer[filformat] = pd.Series(cpr_filer)
        pd.DataFrame.from_dict(filer).to_excel(f'{self.p}\\GDPR_Tjek.xlsx', index=False)