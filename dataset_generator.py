# -*- coding: utf-8 -*-
import json
from pathlib import Path

import typer
from tqdm import tqdm

from datasetgen.generator import Generator
from datasetgen.ui import start_app

app = typer.Typer(name="dataset-generator", add_completion=False)


@app.command()
def ui(dest_folder: str = "dataset", debug: bool = typer.Option(False, "--debug")):
    cur_dest_folder = Path(".").parent.resolve().joinpath(dest_folder)
    start_app(
        debug=debug,
        dest_folder=cur_dest_folder,
    )


@app.command()
def gen(config: str, dest_folder: str = "dataset", num_days: int = -1):
    cur_dest_folder = Path(".").parent.resolve().joinpath(dest_folder)
    with open(Path(config)) as config_file:
        sim_config = json.load(config_file)
    if dest_folder != "":
        cur_dest_folder = Path(
            ".").parent.resolve().joinpath(dest_folder)
    elif 'dest_folder' in config:
        cur_dest_folder = Path(".").parent.resolve().joinpath(
            sim_config['dest_folder'])
    else:
        cur_dest_folder = Path(
            ".").parent.resolve().joinpath("dataset")
    generator = Generator(
        config=sim_config,
        num_days=num_days,
        dest_folder=cur_dest_folder,
    )
    with tqdm(desc="Prepare dataset days", total=100, ascii=True) as pbar:
        prev_perc = 0.
        for cur_perc in generator.prepare(**sim_config['function']):
            pbar.update(int(cur_perc - prev_perc))
            prev_perc = cur_perc

    for _ in tqdm(generator.save(),
                  desc="Save dataset",
                  total=int(generator.num_days),
                  ascii=True):
        pass


if __name__ == "__main__":
    app(prog_name="dataset-generator")
