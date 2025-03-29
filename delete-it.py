#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import QTimer

class MyWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.old_button = QPushButton("Old Button", self)
		self.old_button.clicked.connect(self.on_old_button_clicked)

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.old_button)

		QTimer.singleShot(5000, self.replace_button)

	def on_old_button_clicked(self):
		print("Old button clicked")
		print(f'sender name {self.sender()}')
		print(f'object name {self.sender().objectName()}')
		print(f'old button {self.old_button}')

	def on_new_button_clicked(self):
		print("New button clicked")
		print(f'sender name {self.sender()}')
		print(f'object name {self.sender().objectName()}')
		print(f'old button {self.old_button}')

	def replace_button(self):
		self.new_button = QPushButton("New Button", self)
		self.new_button.clicked.connect(self.on_new_button_clicked)

		self.layout.replaceWidget(self.old_button, self.new_button)
		self.old_button.deleteLater()
		self.old_button = self.new_button


if __name__ == '__main__':
	app = QApplication([])
	widget = MyWidget()
	widget.show()
	app.exec()
