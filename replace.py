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
		print(f'object name is {self.button2.objectName()}')
		self.button2.setObjectName('test2')
		print(f'object name is {self.button2.objectName()}')
		print(f'button2 text {self.button2.text()}')
		#print(f'test2 text{self.test2.text()}')

		layout = QVBoxLayout(self)
		layout.addWidget(self.button1)
		layout.addWidget(self.button2)
		#print('Before')
		#for btn in self.findChildren(QPushButton):
		#	print(btn.objectName(), btn)

	def replace_buttons(self):
		# Replace button1
		index = self.layout().indexOf(self.button1)
		self.layout().removeWidget(self.button1)
		self.button1.deleteLater()
		self.button1 = MyPushButton("New 1")
		self.button1.setObjectName('willie')
		self.layout().insertWidget(index, self.button1)
		child = self.findChild(MyPushButton, 'willie')
		child.clicked.connect(self.child)
		print(f'child {child}')

		# Replace button2
		index = self.layout().indexOf(self.button2)
		#print(f'object name is {self.button2.objectName()}')

		self.layout().removeWidget(self.button2)
		self.button2.deleteLater()
		self.button2 = MyPushButton("New 2")
		self.button2.setObjectName('test2')
		self.layout().insertWidget(index, self.button2)
		#print(f'object name is {self.button2.objectName()}')
		self.button2.pressed.connect(self.click)

		#print('After')
		#for btn in self.findChildren(QPushButton):
		#	print(btn.objectName(), btn)

	def child(self):
		print(f'sender {self.sender().objectName()}')

	def click(self):
		self.button2.text()

	def old_click(self):
		print('old clicked')

if __name__ == "__main__":
	app = QApplication([])
	window = MyWindow()
	window.show()
	app.exec()
