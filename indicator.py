#!/usr/bin/env python3

import sys, os

# disable cache usage must be before any local imports
sys.dont_write_bytecode = True

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QColor
from PyQt6 import uic

import led

class main(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi(os.path.join(os. getcwd(), 'indicator.ui'), self)
		self.setGeometry(50, 50, 300, 300)
		self.setWindowTitle("PyQT6 Indicator Buttons!")

		with open('style.qss','r') as fh:
			self.setStyleSheet(fh.read())

		self.setup_led_buttons() # must be done before connecting signals
		self.setup_buttons()
		self.show()

	def setup_led_buttons(self):
		for child in self.findChildren(QPushButton):
			if child.property('indicator'):
				prop_dict = {}
				prop_dict['name'] = child.objectName()
				prop_dict['text'] = child.text()
				prop_dict['diameter'] = child.property('diameter') or 15
				prop_dict['right_offset'] = child.property('right_offset') or 5
				prop_dict['top_offset'] = child.property('top_offset') or 5
				prop_dict['on_color'] = child.property('on_color') or QColor(0, 255, 0, 255)
				prop_dict['off_color'] = child.property('off_color') or QColor(125, 0, 0, 255)

				new_button = led.IndicatorButton(**prop_dict)
				# determine layout or not
				layout = child.parent().layout()
				if layout:
					index = layout.indexOf(child)
					if index != -1:
						if isinstance(layout, QGridLayout):
							row, column, rowspan, columnspan = layout.getItemPosition(index)
							layout.addWidget(new_button, row, column, rowspan, columnspan)
						elif isinstance(layout, (QVBoxLayout, QHBoxLayout)):
							layout.removeWidget(child)
							layout.insertWidget(index, new_button)
				else:
					geometry = child.geometry()
					child_parent = child.parent()
					new_button.setParent(child_parent)
					new_button.setGeometry(geometry)
				child.deleteLater()
				new_button.setObjectName(prop_dict['name'])
				setattr(self, prop_dict['name'], new_button) # give the new button the old name

	def setup_buttons(self):
		self.estop_pb.setCheckable(True)
		self.estop_pb.toggled.connect(self.estop_toggle)
		self.power_pb.setCheckable(True)
		self.power_pb.setEnabled(False)
		self.power_pb.toggled.connect(self.power_toggle)
		self.momentary_pb.pressed.connect(self.button_pressed)
		self.momentary_pb.released.connect(self.button_released)
		self.toggle_pb.pressed.connect(self.button_toggle_led)
		self.led_pb.pressed.connect(self.button_toggle_led)
		self.no_layout_pb.clicked.connect(self.button_toggle_led)
		self.print_led_buttons_pb.clicked.connect(self.print_led_buttons)
		self.quit_pb.released.connect(self.close)

	def estop_toggle(self):
		if self.estop_pb.isChecked():
			self.estop_pb.led = True
			self.power_pb.setEnabled(True)
		else:
			self.estop_pb.led = False
			self.power_pb.setEnabled(False)
			self.power_pb.setChecked(False)

	def power_toggle(self):
		if self.power_pb.isChecked():
			self.power_pb.led = True
		else:
			self.power_pb.led = False

	def button_toggle_led(self):
		button = self.sender()
		if hasattr(button, 'led'):
			button.led = not button.led

	def button_pressed(self):
		button = self.sender()
		if hasattr(button, 'led'):
			button.led = True

	def button_released(self):
		button = self.sender()
		if hasattr(button, 'led'):
			button.led = False

	def print_led_buttons(self):
		for button in self.findChildren(QPushButton):
			if hasattr(button, 'led'):
				print(button.objectName())

app = QApplication(sys.argv)
gui = main()
sys.exit(app.exec())

