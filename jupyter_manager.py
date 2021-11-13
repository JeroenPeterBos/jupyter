#!/opt/homebrew/Caskroom/miniforge/base/bin/python

from conda.cli.python_api import Commands, run_command
import click
import subprocess


CONDA_ENVIRONMENT_NAME = "jupyter-env"
CONDA_REQUIREMENTS = [
    "jupyter",
]


@click.group()
def main():
    click.echo("Running main!")


@main.command()
def reset_env():
    click.echo("(Re)setting the conda environment")
    out = run_command(Commands.INFO, "--envs".split())
    if CONDA_ENVIRONMENT_NAME in out[0]:
        run_command(Commands.REMOVE, f"-n {CONDA_ENVIRONMENT_NAME} --all".split())
    run_command(Commands.CREATE, f"-n {CONDA_ENVIRONMENT_NAME}".split() + CONDA_REQUIREMENTS)


@main.command()
@click.argument("kernel")
def install_kernel(kernel):
    click.echo("Installing a conda kernel to jupyter")
    run_command(Commands.INSTALL, f"-n {kernel} ipykernel".split())
    run_command(Commands.RUN, f"-n {kernel} python -m ipykernel install --name {kernel} --user --display-name \"Python({kernel})\"".split())


@main.command()
@click.argument("kernel")
def remove_kernel(kernel):
    click.echo("Removing a conda kernel from jupyter")
    run_command(Commands.RUN, f"-n {CONDA_ENVIRONMENT_NAME} jupyter kernelspec uninstall {kernel} -y".split())


@main.command()
def list_kernels():
    click.echo("Listing the available kernels. You can edit the kernels by opening the kernel.json file in the listed directories.")
    run_command(Commands.RUN, f"-n {CONDA_ENVIRONMENT_NAME} jupyter kernelspec list".split())


if __name__ == "__main__":
    main()
