#!/usr/bin/env python3

import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtWidgets import QGridLayout
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
				name = child.objectName()
				text = child.text()
				diameter = child.property('diameter') or 15
				right_offset = child.property('right_offset') or 5
				top_offset = child.property('top_offset') or 5

				print(f'child {child.objectName()}')
				#print(f'diameter {diameter}')
				#print(f'right_offset {right_offset}')
				#print(f'top_offset {top_offset}')

				button = led.IndicatorButton(text, diameter, right_offset, top_offset)
				# determine layout or not
				layout = child.parent().layout()
				if layout:
					index = layout.indexOf(child)
					#print(f'{child.objectName()} layout {layout}')
					if index != -1:
						if isinstance(layout, QGridLayout):
							row, column, rowspan, columnspan = layout.getItemPosition(index)
							layout.addWidget(button, row, column, rowspan, columnspan)
							child.deleteLater()
							setattr(self, name, button)
				else:
					geometry = child.geometry()
					#print(f'{child.objectName()} geometry {geometry}')

	def setup_buttons(self):
		self.estop_pb.setCheckable(True)
		self.estop_pb.toggled.connect(self.estop_toggle)
		self.power_pb.setCheckable(True)
		self.power_pb.setEnabled(False)
		self.power_pb.toggled.connect(self.power_toggle)
		self.quit_pb.released.connect(self.close)

	def estop_toggle(self):
		if self.estop_pb.isChecked():
			self.estop_pb.led = True
			self.power_pb.setEnabled(True)
		else:
			self.estop_pb.led = False
			self.power_pb.setEnabled(False)

	def power_toggle(self):
		if self.power_pb.isChecked():
			self.power_pb.led = True
		else:
			self.power_pb.led = False

app = QApplication(sys.argv)
gui = main()
sys.exit(app.exec())

