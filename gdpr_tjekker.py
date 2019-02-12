from pathlib import Path
import pandas as pd
import csv
import xlrd
from tqdm import tqdm
from loguru import logger
import requests

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

    loglevel : str
        Logging level for den logfil. Mulige værdier er DEBUG, INFO, WARNING, ERROR og CRITICAL

    Returns
    -------
    GdprTjekker object
    
    """

    def __init__(self, path, extensions, encoding='latin1', search_string='', loglevel='WARNING'):
        self.p = Path(path)
        self.extensions = extensions
        self.search_string = search_string
        self.encoding = encoding
        logger.add(Path.joinpath(self.p, 'GDPR_TJEK_{time:DD-MM-YY}.log'), level=loglevel, format='{level} | {time:DD-MM-YYYY kl HH:mm:ss} | {message}')

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
        logger.info(f'Henter liste over alle {extension} filer')
        results = []
        all_files = list(self.p.rglob(f'*.{extension}')) 

        for file in all_files:
            if self.search_string in file.name.lower():
                results.append(file)
        
        return results

    def tjek_cpr(self, filepath):
        """Tjekker om der er en kolonne, som hedder noget med 'cpr'.

        Parameters
        ----------
        filepath : str
            Stien til den fil, som skal kigges i
        
        Returns
        -------
        bool
            True hvis filen indeholder en kolonne, som hedder noget med 'cpr', ellers False
        """
        if Path(filepath).suffix == '.csv' and Path(filepath).name.startswith('~') == False:
            try:
                df = pd.read_csv(filepath, encoding=self.encoding, sep=None, engine='python')
                cpr_file = False
                for col in df.columns:
                    if self.tjek_column_name(col):
                        cpr_file = True
                        break
                return cpr_file
            except (pd.errors.ParserError, csv.Error) as e:
                logger.error(f'{filepath} kan ikke åbnes pga. {e}')
                return e
        elif Path(filepath).suffix == '.xlsx' and Path(filepath).name.startswith('~') == False:
            try:
                df = pd.read_excel(filepath)
            except (xlrd.biffh.XLRDError, PermissionError, FileNotFoundError) as e:
                logger.error(f'{filepath} kan ikke åbnes pga. {e}')
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
        logger.info(f'{filepath} slettet')
    
    def write_to_xlsx(self):
        """Skriver resultaterne ned i en excelfil

        Returns
        -------
        En fil med navnet GDPR_TJEK.xlsx, som ligger i roden.
        """
        filer = {key: None for key in self.extensions}

        for filformat in self.extensions:
            cpr_filer = []
            files = self.get_filepaths(filformat)
            for file in tqdm(files):
                if self.tjek_cpr(file):
                    cpr_filer.append(file)
            filer[filformat] = pd.Series(cpr_filer)
        pd.DataFrame.from_dict(filer).to_excel(Path.joinpath(self.p, 'GDPR_Tjek.xlsx'), index=False)
        logger.info(f"{Path.joinpath(self.p, 'GDPR_Tjek.xlsx')} gemt!")

    def send_file_to_mail(self, mailgun_api_key, mailgun_domain_name, email_adress):
        """Sender en mail til en given email adresse med resultaterne fra analysen. Man skal have en account hos Mailgun. Den er gratis.

        parameters
        ----------
        mailgun_api_key : str
            En api key fra Mailgun.

        mailgun_domain_name : str
            Domain name fra Mailgun.
        
        email_adress : str
            Den email adresse resultaterne skal sendes til.
        
        Raises
        ------
        FileNotFoundError
            Hvis resultat filen 'GDPR_Tjek.xlsx' ikke eksisterer, så sendes der ingen mail.
        """
        try: 
            logger.info(f'Sendt til {email_adress}')
            return requests.post(
                f'https://api.mailgun.net/v3/{mailgun_domain_name}/messages',
                auth=('api', mailgun_api_key),
                data={
                    'from': f'GDPR Tjekker <mailgun@{mailgun_domain_name}>',
                    'to': [email_adress],
                    'subject': f'Filer med cpr-numre i {self.p}',
                    'text': f'''
                        Hej.

                        Her får du en liste over de excel og/eller csv filer på {self.p}, som muligvis indeholder cpr-numre.

                        Hilsen
                        GDPR Tjekkeren.
                    '''
                },
                files=[('attachment', ('GDPR_Tjek.xlsx', open(Path.joinpath(self.p, 'gdpr_tjek.xlsx'), 'rb').read()))],
            )
        except FileNotFoundError as e:
            logger.error(e)
