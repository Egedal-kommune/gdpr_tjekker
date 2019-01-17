import click
from gdpr_tjekker import GdprTjekker

@click.command(help='Tjek efter xlsx og/eller csv filer, som indeholder cpr data. PATH er stien til den folder, der skal tjekkes, og EXTENSIONS er en eller flere filformater')
@click.argument('path')
@click.argument('extensions', nargs=-1)
@click.option('--encoding', '-e', default='latin1')
@click.option('--search_string', '-s', default='')
@click.option('--loglevel', '-l', default='WARNING')
def main(path, extensions, encoding, search_string, loglevel):
    filformater = [i for i in extensions]
    sniffer = GdprTjekker(path, [i for i in extensions], encoding, search_string, loglevel)
    sniffer.write_to_xlsx()

if __name__ == "__main__":
    main()