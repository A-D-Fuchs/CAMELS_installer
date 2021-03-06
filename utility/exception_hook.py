import os.path
from traceback import print_tb
from PyQt5.QtWidgets import QMessageBox

import logging

from utility.load_save_functions import appdata_path

if not os.path.isfile(f'{appdata_path}/logging.log'):
	with open(f'{appdata_path}/logging.log', 'w'):
		pass
logging.basicConfig(filename=f'{appdata_path}/logging.log', level=logging.DEBUG)


class ErrorMessage(QMessageBox):
	"""A popUp-box describing the Error."""
	def __init__(self, msg, info_text='', parent=None):
		super().__init__(parent)
		self.setWindowTitle('ERROR')
		self.setIcon(QMessageBox.Warning)
		self.setStandardButtons(QMessageBox.Ok)
		self.setText(msg)
		if info_text:
			self.setInformativeText(info_text)


def exception_hook(*exc_info):
	"""Use to overwrite sys.excepthook, so that an exception does not
	terminate the program, but simply shows a Message with the exception."""
	if issubclass(exc_info[0], KeyboardInterrupt):
		return
	logging.exception(str(exc_info))
	ErrorMessage(exc_info[0].__name__, str(exc_info[1]) + '\n' + str(print_tb(exc_info[2]))).exec_()