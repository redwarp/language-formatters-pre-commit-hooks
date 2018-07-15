from __future__ import print_function

import argparse
import sys
from commands import getstatusoutput


def pretty_format_golang(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    status, output = getstatusoutput(
        'gofmt{} -l {}'.format(
            ' -w' if args.autofix else '',
            ' '.join(args.filenames),
        ),
    )

    if status != 0:  # pragma: no cover
        # This is possible if gofmt is not available on the path, most probably because go is not available
        print(output)
        return 1

    status = 0
    if output:
        status = 1
        if args.autofix:
            print('The following files have been fixed by gofmt: {}'.format(
                ', '.join(output.splitlines()),
            ))
        else:
            print('The following files are not properly formatted: {}'.format(
                ', '.join(output.splitlines()),
            ))

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_golang())