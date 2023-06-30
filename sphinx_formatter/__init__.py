import argparse
import pyperclip
import re


def format_excel_text(output_type=0):
    if output_type == 0:
        text = pyperclip.paste()
        output = re.sub(r'\r\n(?!$)', r'\n   * - ', text)
        output = output.replace('\t', '\n     - ')
        output = '.. list-table:: Title\n   :header-rows: 1\n\n   * - ' + output
        return output
    else:
        pass

def main():
    parser = argparse.ArgumentParser(
        description='a command line to format string to Restructured Text')

    subparsers = parser.add_subparsers(help='sub-commands help',
                                       dest='command')

    parser_table = subparsers.add_parser(
        'table',
        help='format clipboard string as table'
    )
    parser_table.add_argument('-t',
                              '--type',
                              help='the type of string, such as "excel"')
    args = parser.parse_args()
    if args.command == 'table':
        if args.type == 'excel':
            output = format_excel_text()
            pyperclip.copy(output)
            print(output)
