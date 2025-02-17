import traceback
import subprocess

import click
from rich.console import Console

from landaulang.analyzer import build_symtable
from landaulang.lexer import LandauLexer
from landaulang.parser import LandauParser
from landaulang.trans2py import transpy
from landaulang.utils import CommandManager, print_message

console = Console()


@click.group()
def cli():
	"""
	Small 'home' programming language (name is given in honor of soviet scientist Lev D. Landau)
	"""
	pass


@cli.command()
@click.argument("filename")
@click.option(
	"--output",
	"-o",
	default="{filename}.py",
	help="Name for output python program. You can use formatting: {filename} for get filename",
)
@click.option("--printprog", is_flag=True, help="print result program", default=True)
def convert2py(filename: str, output: str, printprog: bool = True):
	with open(filename, "r") as file:
		text = file.read()

	tokens = LandauLexer().tokenize(text)
	ast = LandauParser().parse(tokens)
	build_symtable(ast)
	program = transpy(ast)

	output = output.format(filename=filename)

	if printprog:
		console.print(program)

	with open(output, "w") as file:
		file.write(program)


@cli.command()
@click.argument("filename")
@click.option(
	"--output",
	"-o",
	default="{filename}_out.py",
	help="Name for output python program. You can use formatting: {filename} for get filename",
)
def exec(filename: str, output: str):
	status = True
	message = 'landaulang'

	with open(filename, "r") as file:
		text = file.read()

	tokens = LandauLexer().tokenize(text)
	ast = LandauParser().parse(tokens)
	build_symtable(ast)
	program = transpy(ast)

	output = output.format(filename=filename)

	with open(output, "w") as file:
		file.write(program)

	try:
		CommandManager.run_command(f'python {output}')
		print()
	except:
		message = traceback.format_exc()
		status = False
		print_message('error', f'Message: {message}')
	else:
		print_message('info', 'Successfully executed!')

	with open(output, 'a') as file:
		file.write('\n\n# status: {status}\n# {message}')


def main():
	cli()


if __name__ == "__main__":
	main()
