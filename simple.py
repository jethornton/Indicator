#!/usr/bin/env python3

import sys, os

from PyQt6.QtCore import Qt, pyqtProperty, QPointF, QEvent
from PyQt6.QtGui import QRadialGradient, QPainter, QColor, QBrush, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6 import uic

class IndicatorButton(QPushButton):
	_led = False

	def __init__(self, text='none', diameter=15):
		super().__init__()
		#print(diameter)
		self.diameter = int(diameter)
		self.text = text
		#print(self._led)

	def paintEvent(self, event):
		super().paintEvent(event)
		self.setText(self.text)
		painter = QPainter(self)
		size = self.rect()
		x_offset = 12
		x_center = size.width() - ((self.diameter / 2) + x_offset)
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
		else:
			gradient.setColorAt(1, off_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(off_color)
			painter.drawEllipse(QPointF(x_center, y_center), self.diameter / 2, self.diameter / 2)

	def setLed(self, val):
		self._led = val
		self.update()

	def getLed(self):
		self.update()
		return self._led

	led = pyqtProperty(bool, getLed, setLed)


class main(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi(os.path.join(os. getcwd(), 'simple.ui'), self)
		self.setGeometry(150, 150, 150, 150)
		self.setWindowTitle("PyQT6 Indicator Buttons!")

		self.estop_pb.toggled.connect(self.indicator)
		self.power_pb.clicked.connect(self.test)
		self.quit_pb.released.connect(self.close)

		self.setup_leds()

		self.show()

	def setup_leds(self):
		for child in self.findChildren(QPushButton):
			if child.property('indicator'):
				name = child.objectName()
				print(name)
				text = child.text()
				checkable = child.isCheckable()
				layout = child.parent().layout()
				index = layout.indexOf(child)


	def indicator(self):
		button = self.sender()
		if hasattr(button, 'led'):
			if button.isChecked():
				button.led = True
			else:
				button.led = False

	def test(self):
		self.estop_pb.setText('E STOP')

app = QApplication(sys.argv)
gui = main()
sys.exit(app.exec())
