#!/usr/bin/env python3

import sys, os

from PyQt6.QtCore import Qt, pyqtProperty, QPointF, QEvent
from PyQt6.QtGui import QRadialGradient, QPainter, QColor, QBrush, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt6 import uic

class IndicatorButton(QPushButton):
	_led = False

	def __init__(self, text='none', diameter=15):
		super().__init__()
		#print(diameter)
		self.diameter = int(diameter)
		self._text = text
		#print(self._led)

	def paintEvent(self, event):
		super().paintEvent(event)
		self.setText(self._text)
		painter = QPainter(self)
		size = self.rect()
		#print(size.topRight())
		#diameter = 15
		x_offset = 12
		x_center = size.width() - ((self.diameter / 2) + x_offset)
		#print(size.width())
		#print(x_center)
		y_offset = 12
		y_center = (self.diameter / 2) + y_offset
		self._right_edge_offset = 5
		self._top_edge_offset = 5
		on_color = QColor(0, 255, 0, 255)
		off_color = QColor(125, 0, 0, 255)
		x = int(size.width() - self.diameter - self._right_edge_offset)
		y = int(0 + self._top_edge_offset)
		gradient = QRadialGradient(x + self.diameter / 2, y + self.diameter / 2,
			self.diameter * 0.4, self.diameter * 0.4, self.diameter * 0.4)
		gradient.setColorAt(0, Qt.GlobalColor.white)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		if self._led:
			gradient.setColorAt(1, on_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(on_color)
			# Draws the ellipse positioned at center with radii rx and ry.
			painter.drawEllipse(QPointF(x_center, y_center), self.diameter / 2, self.diameter / 2)
			#painter.drawEllipse(x, y, diameter - 1, diameter - 1)
			#painter.fillRect(size.width() - 20, size.height() - 20, 10, 10, QColor(80, 255, 80, 255))
		else:
			gradient.setColorAt(1, off_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(off_color)
			painter.drawEllipse(QPointF(x_center, y_center), self.diameter / 2, self.diameter / 2)
			#painter.drawEllipse(x, y, diameter - 1, diameter - 1)
			#painter.fillRect(size.width() - 20, size.height() - 20, 10, 10, QColor(255, 80, 80, 255))

	def setLed(self, val):
		self._led = val
		#print("Led is set to", val)
		self.update()

	def getLed(self):
		#print("read Led = ", self._led)
		self.update()
		return self._led

	led = pyqtProperty(bool, getLed, setLed)


class main(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi(os.path.join(os. getcwd(), 'indicator.ui'), self)
		self.setGeometry(50, 50, 300, 300)
		self.setWindowTitle("PyQT6 Indicator Buttons!")
		self.print_children_pb.clicked.connect(self.print_children)
		#print('Before')
		#for child in self.findChildren(QPushButton):
		#	print(child)

		for child in self.findChildren(QPushButton):
			if child.property('indicator'):
				property_dict = {} # create a property dictionary
				#print(child.dynamicPropertyNames())
				prop_names = child.dynamicPropertyNames()
				for prop_name in prop_names:
					prop = prop_name.data().decode()
					#print(prop)
					#print(f'property {prop}')
					#print(f'{child.objectName()} {prop} {child.property(prop)}')
					property_dict[prop] = child.property(prop)
				#print(f'{child.objectName()} enabled {child.isEnabled()}')
				property_dict['enabled'] = child.isEnabled()

				name = child.objectName()
				text = child.text()
				checkable = child.isCheckable()
				layout = child.parent().layout()
				index = layout.indexOf(child)
				if index != -1:
					row, column, rowspan, columnspan = layout.getItemPosition(index)
					if 'diameter' in property_dict:
						diameter = property_dict['diameter']
						#print(type(diameter))
						self.button = IndicatorButton(text, diameter)
					else:
						self.button = IndicatorButton(text)
					self.button.setObjectName(name)
					#print(button.parent())
					for key, value in property_dict.items(): # copy properties to new button
						#print(key, value)
						self.button.setProperty(key, value)
					self.button.setEnabled(property_dict['enabled'])
					if checkable:
						self.button.setCheckable(True)
						self.button.toggled.connect(self.indicator)
					else:
						self.button.pressed.connect(self.pressed)
						self.button.released.connect(self.released)
					layout.addWidget(self.button, row, column, rowspan, columnspan)
					child.deleteLater()
					new_button = self.findChild(IndicatorButton, name)
					#print(f'{name} {new_button.objectName()}')
					#setattr(self, name, new_button)
					#print(getattr(self, name).text())
					setattr(self, name, new_button)
					#if name == 'power_pb':
					#	# reassign the new button to the old button
					#	self.power_pb = self.findChild(IndicatorButton, 'power_pb')
					self.power_pb.setEnabled(False)

		self.power_pb.toggled.connect(self.indicator)
		self.quit_pb.released.connect(self.close)

		with open('style.qss','r') as fh:
			self.setStyleSheet(fh.read())
		self.show()

	def print_children(self):
		#print('Children')
		print(self.estop_pb.text())
		self.pushButton.setEnabled(not self.pushButton.isEnabled())
		#for child in self.findChildren(QPushButton):
		#	print(child)

	def pressed(self):
		button = self.sender()
		if hasattr(button, 'led'):
			button.led = True

	def released(self):
		button = self.sender()
		if hasattr(button, 'led'):
			button.led = False

	def indicator(self):
		button = self.sender()
		if hasattr(button, 'led'):
			if button.isChecked():
				button.led = True
			else:
				button.led = False
		button.update()
		if button.objectName() == 'estop_pb':
			if button.isChecked():
				self.power_pb.setEnabled(True)
			else:
				self.power_pb.setEnabled(False)
				self.power_pb.setChecked(False)

app = QApplication(sys.argv)
gui = main()
sys.exit(app.exec())
