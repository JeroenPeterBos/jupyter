#!/usr/bin/env python3

import os
if os.environ.get("CONDA_DEFAULT_ENV", "") != "base":
    raise SystemError(f"Running from the incorrect conda environment. \'{os.environ.get('CONDA_DEFAULT_ENV', '')}\' instead of \'base\'.")

from conda.cli.python_api import Commands, run_command
import click
from shlex import split
import sys


CONDA_ENVIRONMENT_NAME = "jupyter-env"
CONDA_REQUIREMENTS = [
    "jupyter",
    "jupyterlab",
    "nodejs"
]


@click.group()
def main():
    pass


@main.command()
def reset_env():
    click.secho("(Re)setting the jupyter conda environment.", fg='blue')

    click.secho("Removing the old environment.", fg='blue')
    out = run_command(Commands.INFO, "--envs".split())
    if CONDA_ENVIRONMENT_NAME in out[0]:
        run_command(Commands.REMOVE, f"-n {CONDA_ENVIRONMENT_NAME} --all".split(), stdout=sys.stdout)

    click.secho("Installing the new environment.", fg='blue')
    run_command(Commands.CREATE, f"-n {CONDA_ENVIRONMENT_NAME}".split() + CONDA_REQUIREMENTS, stdout=sys.stdout)

    click.secho("Finished.", fg='blue')


@main.command()
@click.argument("kernel")
def install_kernel(kernel):
    click.secho("Installing a conda kernel to jupyter", fg='blue')

    click.secho("Installing ipykernel to the conda kernel.", fg='blue')
    run_command(Commands.INSTALL, split(f"-n {kernel} ipykernel"), stdout=sys.stdout)

    click.secho("Creating a kernel spec for jupyter.", fg='blue')
    python_version = run_command(Commands.RUN, split(f"-n {kernel} python --version"))[0].strip().replace("Python", "Py")
    run_command(Commands.RUN, split(f"-n {kernel} python -m ipykernel install --name {kernel} --user --display-name \"{kernel} ({python_version})\""), stdout=sys.stdout)

    click.secho("Finished.", fg='blue')


@main.command()
@click.argument("kernel")
def remove_kernel(kernel):
    click.secho("Removing a conda kernel from jupyter", fg='blue')

    click.secho("Removing the kernel spec for jupyter.", fg='blue')
    run_command(Commands.RUN, split(f"-n {CONDA_ENVIRONMENT_NAME} jupyter kernelspec uninstall {kernel} -y"), stdout=sys.stdout)

    click.secho("Finished.", fg='blue')


@main.command()
def list_kernels():
    click.secho("Listing the available kernels. You can edit the kernels by opening the kernel.json file in the listed directories.", fg='blue')

    click.secho("Listing the jupyter kernels.", fg='blue')
    run_command(Commands.RUN, split(f"-n {CONDA_ENVIRONMENT_NAME} jupyter kernelspec list"))

    click.secho("Finished.", fg='blue')


if __name__ == "__main__":
    main()
