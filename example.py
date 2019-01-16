from gdpr_tjekker import GdprTjekker
import pandas as pd
from tqdm import tqdm

# Indsæt sti til den folder, som skal tjekkes igennem
tjekker = GdprTjekker(STI TIL FOLDER)

filformater = ['xlsx', 'csv']

filer = {key: None for key in filformater}

for filformat in filformater:
    cpr_filer = []
    files = tjekker.get_filepaths(filformat, '')
    for file in tqdm(files):
        if tjekker.tjek_cpr(file, encoding='latin1'):
            cpr_filer.append(file)
    filer[filformat] = pd.Series(cpr_filer)

df = pd.DataFrame.from_dict(filer)
df.to_excel(f'{tjekker.p}\\GDPR_TJEK.xlsx', index=False)