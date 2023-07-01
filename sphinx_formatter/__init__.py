import argparse
import pyperclip
import re

from wcwidth import wcswidth


def get_str_width(text):
    """Get string width.

    Using wcswith to get the text width.
    Because function len() to get the text width
    sometimes is incorrect, if the text include
    unicode character.
    """
    if not isinstance(text, str):
        type_name = type(text).__name__
        raise TypeError(f'Parameter text must be str type! not {type_name}!')
    return sum(wcswidth(c) for c in text)


def format_excel_text(output_type='0', no_include_header=False):
    text = pyperclip.paste()
    if output_type == '0':
        output = re.sub(r'\r\n(?!$)', r'\n   * - ', text)
        output = output.replace('\t', '\n     - ')
        output = [
            '.. list-table:: Title\n',
            '   :header-rows: 1\n',
            '\n   * - ',
            output
        ]
        if no_include_header:
            output.pop(1)
        output = ''.join(output)
        return output
    else:
        text = re.sub(r'\r\n$', '', text)
        output = ''
        table = []
        column_max_length = {}
        for row_values in text.split('\r\n'):
            _t = []
            for column, column_value in enumerate(row_values.split('\t')):
                column_value = column_value.strip()
                _t.append(column_value)
                max_length = column_max_length.get(column, -1)
                column_length = get_str_width(column_value)
                if max_length == -1 or column_length > max_length:
                    column_max_length[column] = column_length
            table.append(_t)
        output = ''
        for row_index, row in enumerate(table):
            _row_values = ''
            _row_paddings = ''
            for column_index, value in enumerate(row):
                max_length = column_max_length[column_index]
                value_length = get_str_width(value)
                padding_width = max_length - value_length
                _row_values += '| ' + value + ' ' * padding_width + ' '
                _row_paddings += '+' + '-' * (max_length + 2)
            if len(output) == 0:
                output += _row_paddings + '+\n'
            if row_index == 0 and not no_include_header:
                _row_paddings = _row_paddings.replace('-', '=')
            output += _row_values + '|\n'
            output += _row_paddings + '+\n'
        return output


def main():
    parser = argparse.ArgumentParser(
        description='a command line to format string to Restructured Text for sphinx'
    )

    subparsers = parser.add_subparsers(
        help='sub-commands help',
        dest='command'
    )
    parser_table = subparsers.add_parser(
        'table',
        help='format clipboard string as Restructured Text table'
    )
    parser_table.add_argument(
        '-o',
        '--output-type',
        help='set output type, [0, 1] supported. Default is 1.'
    )
    parser_table.add_argument(
        '--dry-run',
        action='store_true',
        help='run and show the result, but not copy the result to clipboard'
    )
    parser_table.add_argument(
        '--no-include-header',
        action='store_true',
        help='the input data not include table header, default is False'
    )

    args = parser.parse_args()
    if args.command == 'table':
        output = format_excel_text(args.output_type, args.no_include_header)
        print(output)
        if args.dry_run:
            print(
                '\nDry run mode: the data above has NOT copied to the clipboard.\n')
        else:
            pyperclip.copy(output)
            print('\nAll the data has copied. You can use '
                  '[ctrl+v] to paste data to the editor.\n')
