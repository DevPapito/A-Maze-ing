import sys
from .exceptions_parser import ExceptionParser, ExceptionLengthParser, ExceptionNameParser
from .config_interpretor import interpretor

def file_validate():
	try:
		with open("config.txt", "r") as file:
			pass
	except FileNotFoundError:
		print("File <config.txt> not found in the directory!")
		sys.exit(1)
	except PermissionError:
		print("Permission denied to open/read file <config.txt>")
		sys.exit(1)
	except Exception as e:
		print(e)
		sys.exit(1);

def argument_validate():
	try:
		if (len(sys.argv) != 2):
			raise ExceptionLengthParser()
		if (sys.argv[1] != "config.txt"):
			raise ExceptionNameParser()
	except ExceptionNameParser as e:
		print(e)
		sys.exit(1)
	except ExceptionLengthParser as e:
		print(e)
		sys.exit(1)
	except ExceptionParser as e:
		print(e)
		sys.exit(1)

def parser(): # Retorna o dado parsealizado com (sanatizatior/validation) ideal
	argument_validate()
	file_validate()
	config: Dict[str, str] = interpretor()
	print(config)
	# Afirmar que o dataclass nao seja alterado em processo nao esperado
	# parser deve afirmar esse contrato de retornar o Dataclass corretamente - pos-condition
