#!/usr/bin/env python3

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal

class CustomButton(QPushButton):
	custom_signal = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self.clicked.connect(self.on_click)

	def on_click(self):
		self.custom_signal.emit()

	def mousePressEvent(self, event):
		super().mousePressEvent(event)
		# Add custom behavior on mouse press
		print("Custom button pressed")

# Example: Replacing a button in a layout
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class MyWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.layout = QVBoxLayout(self)
		self.button1 = QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.custom_button = CustomButton("Custom Button")
		self.replace_button(self.button1, self.custom_button)

	def replace_button(self, old_button, new_button):
		index = self.layout.indexOf(old_button)
		self.layout.removeWidget(old_button)
		old_button.deleteLater() 
		self.layout.insertWidget(index, new_button)

# Example: Using the widget
if __name__ == '__main__':
	from PyQt6.QtWidgets import QApplication
	import sys
	app = QApplication(sys.argv)
	window = MyWidget()
	window.show()
	sys.exit(app.exec())

