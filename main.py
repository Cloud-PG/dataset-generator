# -*- coding: utf-8 -*-
import argparse
import json
from pathlib import Path

from tqdm import tqdm

from datasetgen.generator import Generator
from datasetgen.ui import start_app
from datasetgen.utils import str2bool


def main():
    parser = argparse.ArgumentParser(description='Dataset Generator')
    parser.add_argument('--ui', action='store_true',
                        help='use the graphic user interface')
    parser.add_argument('--ui-debug', type=str2bool, default=True,
                        help='use the graphic user interface in debug mode')
    parser.add_argument('--num-days', type=int, default=1,
                        help='total number of days to create')
    parser.add_argument('--dest-folder', type=str, default="dataset",
                        help='name of the output folder')
    parser.add_argument('--config', type=str, default="./config.json",
                        help='path of the configuration file in JSON format')

    args = parser.parse_args()

    if args.ui:
        start_app(
            debug=args.ui_debug,
            dest_folder=Path(".").parent.resolve().joinpath(args.dest_folder),
        )
    else:
        with open(Path(args.config)) as config_file:
            config = json.load(config_file)
        generator = Generator(
            config=config,
            num_days=args.num_days,
            dest_folder=Path(".").parent.resolve().joinpath(args.dest_folder),
        )
        for _ in tqdm(generator.prepare(),
                      desc="Prepare dataset", 
                      total=generator.num_days, 
                      ascii=True):
            pass
        for _ in tqdm(generator.save(),
                      desc="Save dataset", 
                      total=generator.num_days, 
                      ascii=True):
            pass


if __name__ == "__main__":
    exit(main())
