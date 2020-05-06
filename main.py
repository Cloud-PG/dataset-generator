# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

from datasetgen.ui import start_app
from datasetgen.utils import str2bool


def main():
    parser = argparse.ArgumentParser(description='Dataset Generator')
    parser.add_argument('--ui', action='store_true',
                        help='use the graphic user interface')
    parser.add_argument('--ui-debug', type=str2bool, default=True,
                        help='use the graphic user interface in debug mode')
    parser.add_argument('--dest-folder', type=str, default="dataset",
                        help='name of the output folder')

    args = parser.parse_args()

    if args.ui:
        start_app(
            debug=args.ui_debug,
            dest_folder=Path(".").parent.resolve().joinpath(args.dest_folder),
        )
    else:
        parser.print_usage()


if __name__ == "__main__":
    exit(main())
