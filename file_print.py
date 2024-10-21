import subprocess
import logging_module as logger

def file_print(filePath, printer):
    print('lp / -d ' + printer + ' / ' + "'" + filePath + "'")
    # subprocess.run(["lpr", "-P " + printer, filePath]) #check whitespace before usage
    subprocess.run(["/usr/bin/lp", "-d" + printer, filePath])
    print('sent file to printer', printer)
