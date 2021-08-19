'''
THIS PROGRAM CLEANS THE TEMP FOLDER ON WINDOWS
'''

from os import walk, remove
from os.path import getsize, join, isfile, isdir
from threading import Timer
from shutil import rmtree
from json import load
from datetime import datetime
from sys import exit
from utils import create_file, clean_file, file_write

class Cleaner:

	def __init__(self):

		self.TEMP_path, self.interval = self.get_file_data()

		self.get_report(*self.clean_folder())

		if self.interval == 0:
			raise SystemExit

	def set_timer(self):

		timer = Timer(self.interval, lambda: self.get_report(*self.clean_folder()))
		timer.start()

	def get_file_data(self):

		try:
			with open('data.json') as file:
				data = load(file)
			if not isdir(data['temp_path']) or not isinstance(data['interval'], int):
				raise SystemExit
			elif data['interval'] <= 0:
				raise SystemExit
			return data['temp_path'], data['interval']
		except (FileNotFoundError, KeyError):
			raise SystemExit

	def clean_folder(self):

		files_size = 0
		errors_log = ''

		for adress, dirs, files in walk(self.TEMP_path):
			for file in files:
				path = join(adress, file)
				try:
					size = getsize(path)
					remove(path)
					files_size += size
				except FileNotFoundError:
					errors_log += f'\nFile: {path}\nError type: file was renamed, deleted or replaced'
					continue
				except PermissionError:
					errors_log += f'\nFile: {path}\nError type: permission error'
					continue

		for adress, dirs, files in walk(self.TEMP_path):
			for dir in dirs:
				try:
					rmtree(join(adress, dir))
				except FileNotFoundError:
					errors_log += f'\nDirectory: {path}\nError type: directory was renamed, deleted or replaced'
					continue
				except PermissionError:
					errors_log += f'\nDirectory: {path}\nError type: permission error'
					continue

		if self.interval != 0:
			self.set_timer()

		return files_size, errors_log	

	def get_report(self, size, errors, file='cleanReport.txt'):

		index = 0
		measure_list = ('b', 'Kb', 'Mb')
		size_measure = measure_list[index]

		while size / 1024 > 1 and size_measure != measure_list[-1]:

			size /= 1024
			index += 1
			size_measure = measure_list[index]

		time = datetime.now().strftime('%m.%d.%Y %H:%M:%S')
		report_data = f'Report date: {time}\nCleaned size: {round(size, 1)} {size_measure}'

		if errors:
			report_data += f'\nErrors while removing:{errors}'

		if not isfile(file):
			create_file(file)
		else:
			if getsize(file) > 10_485_760:
				clean_file(file)

		file_write(file, report_data + '\n\n', 'a')

if __name__ == '__main__':

	try:
		cleaner = Cleaner()
	except:
		exit()