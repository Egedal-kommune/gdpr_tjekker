import click
import os
from gdpr_tjekker import GdprTjekker

@click.command(help='Tjek efter xlsx og/eller csv filer, som indeholder cpr data. PATH er stien til den folder, der skal tjekkes, og EXTENSIONS er en eller flere filformater')
@click.argument('path')
@click.argument('extensions', nargs=-1)
@click.option('--encoding', '-e', default='latin1', show_default=True)
@click.option('--search_string', '-s', default='', show_default=True)
@click.option('--loglevel', '-l', default='WARNING', show_default=True)
@click.option('--email', '-m', default='', show_default=True)
def main(path, extensions, encoding, search_string, loglevel, email):
    filformater = [i for i in extensions]
    sniffer = GdprTjekker(path, [i for i in extensions], encoding, search_string, loglevel)
    sniffer.write_to_xlsx()
    if email != '':
        sniffer.send_file_to_mail(os.environ['MAILGUN_API_KEY'], os.environ['MAILGUN_DOMAIN_NAME'], email)

if __name__ == "__main__":
    main()