from colorama import Fore, init
from os.path import isdir
from json import dumps
from sys import exit
from utils import file_write

class Dumper:

	def __init__(self):

		init()
		
		self.data = {}

	def input_path(self):

		print(f'{Fore.WHITE}Enter path to {Fore.YELLOW}Temp {Fore.WHITE}directory')
		while True:

			temp_path = input(f'>>> ')

			if not isdir(temp_path):
				print(f'{Fore.RED}Invalid path to directory{Fore.WHITE}\n')
			else:
				self.data.update({'temp_path' : temp_path})
				break

	def input_interval(self):
		
		print(f'{Fore.WHITE}Enter the interval ({Fore.YELLOW}in minutes{Fore.WHITE}) for clean directory, {Fore.YELLOW}0 {Fore.WHITE}- to clean one time')
		while True:
			try:
				interval = int(input('>>> '))
				if interval < 0:
					raise ValueError
			except ValueError:
				print(f'{Fore.RED}Invalid interval{Fore.WHITE}\n')
				continue
			else:
				self.data.update({'interval' : interval * 60})
				break

	def dump_data(self):

		file_write('data.json', dumps(self.data))
		print(f'\n{Fore.GREEN}Data was successfully uploaded{Fore.WHITE}')

	def start(self):

		self.input_path()
		self.input_interval()
		self.dump_data()

if __name__ == '__main__':

	try:
		dumper = Dumper()
		dumper.start()
	except (KeyboardInterrupt, SystemExit):
		exit()
	finally:
		try:
			input('\nPress enter to exit\n')
		except:
			exit()