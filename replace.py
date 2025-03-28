#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MyPushButton(QPushButton):
	def __init__(self, text, parent=None):
		super().__init__(text, parent)
		# Add custom initialization or behavior here
		self.clicked.connect(self.on_click)

	def on_click(self):
		print(f"Button '{self.text()}' clicked")

class MyWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.button1 = QPushButton("Old 1")
		self.button1.clicked.connect(self.replace_buttons)
		self.button2 = QPushButton("Old 2")
		self.button2.clicked.connect(self.old_click)

		layout = QVBoxLayout(self)
		layout.addWidget(self.button1)
		layout.addWidget(self.button2)
		print('Before')
		for btn in self.findChildren(QPushButton):
			print(btn)

		#self.replace_buttons()

	def replace_buttons(self):
		# Replace button1
		index = self.layout().indexOf(self.button1)
		self.layout().removeWidget(self.button1)
		self.button1.deleteLater()
		self.button1 = MyPushButton("New 1")
		self.layout().insertWidget(index, self.button1)

		# Replace button2
		index = self.layout().indexOf(self.button2)
		self.layout().removeWidget(self.button2)
		self.button2.deleteLater()
		self.button2 = MyPushButton("New 2")
		self.layout().insertWidget(index, self.button2)
		self.button2.clicked.connect(self.click)

		print('After')
		for btn in self.findChildren(QPushButton):
			print(btn)

	def click(self):
		print('replaced_clicked')

	def old_click(self):
		print('old clicked')

if __name__ == "__main__":
	app = QApplication([])
	window = MyWindow()
	window.show()
	app.exec()
