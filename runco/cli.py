# -*- coding: utf-8 -*-

import click
import logging
import sys
import os
from runco import config

@click.command()
def main(files=None):
    logging.basicConfig(level=logging.INFO)


@click.command()
def generate_runco_config():
  logging.basicConfig(level=logging.DEBUG)
  c = config.Config()


if __name__ == "__main__":
    main()