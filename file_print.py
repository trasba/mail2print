import click, subprocess

def file_print(filePath, printer):
    print('lp / -d ' + printer + ' / ' + "'" + filePath + "'")
    # subprocess.run(["lpr", "-P " + printer, filePath]) #check whitespace before usage
    subprocess.run(["/usr/bin/lp", "-d" + printer, filePath])
    print('sent file to printer', printer)

### click section for cli interface
@click.command()
@click.option('--path', prompt='file path',
              help='The path to the file to print')
@click.option('--printer', prompt='printer name',
              help='The printer to print on')

def file_print_cli(path, printer):
    """
    Helper function as cli interface
    """
    file_print(path, printer)

if __name__ == '__main__':
    file_print_cli()
