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