# GDPR Tjekker

Et lille script, som kan søge igennem en folder efter csv eller excel filer, som indeholder en kolonne med cpr numer.

### Eksempel:

Import GdprTjekker class og lav et nyt object, som peger på den sti, du vil kigge på, og hvilken filformater, der skal kigges efter.
```Python
from gdpr_tjekker import GdprTjekker

sniffer = GpdrTjekker('Q:\CBK', ['csv', 'xlsx'], encoding='latin1')
```
__HUSK__ at tilføje, hvilken encoding filerne er, der søges igennem (Default er _latin1_)

skriv resultatet af søgningen i en excelfil, som bliver gemt på den sti, som søges igennem.
```Python
sniffer.write_to_xlsx()
```

#### CLI
Værktøjet kan også bruges som et cli-tool.

```Bash
Usage: gdpr_tjekker_cli.py [OPTIONS] PATH [EXTENSIONS]...

  Tjek efter xlsx og/eller csv filer, som indeholder cpr data. PATH er stien
  til den folder, der skal tjekkes, og EXTENSIONS er en eller flere
  filformater

Options:
  -e, --encoding TEXT
  -s, --search_string TEXT
  -l, --loglevel TEXT
  --help                    Show this message and exit.
```
F.eks. hvis man vil søge igennem et drev til at finde alle excel og csv filer, der hedder noget med _Høringsliste_ i stien C:\user\desktop, så ville man skrive:

```Bash
python gdpr_tjekker_cli.py -s Høringsliste C:\user\desktop xlsx csv
```
Hvis man kun vil søge efter xlsx eller csv, så skriver man kun et filformat.

Den kigger så stien igennem og laver to filer på C:\user\desktop. En som hedder GDPR_Tjek.xlsx og en, som hedder GDPR_TJEK_**TIDSPUNKT**.log