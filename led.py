
from PyQt6.QtCore import Qt, pyqtProperty, QPointF, QEvent
from PyQt6.QtGui import QRadialGradient, QPainter, QColor, QBrush, QPainter
from PyQt6.QtWidgets import QPushButton

class IndicatorButton(QPushButton):
	_led = False

	def __init__(self, txt, dia, r_offset, t_offset):
		super().__init__()
		#print(diameter)
		self.setText(txt)
		self._text = txt
		self._diameter = dia
		self._top_offset = t_offset
		self._right_offset = r_offset
		#print(f'text {type(self._text)} {self._text}')
		#print(f'diameter {type(self._diameter)} {self._diameter}')
		#print(f'top_offset {type(self._top_offset)} {self._top_offset}')
		#print(f'right_offset {type(self._right_offset)} {self._right_offset}')

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		x_center = size.width() - ((self._diameter / 2) + self._right_offset)
		y_center = (self._diameter / 2) + self._top_offset
		on_color = QColor(0, 255, 0, 255)
		off_color = QColor(125, 0, 0, 255)
		x = int(size.width() - self._diameter - self._right_offset)
		y = int(0 + self._top_offset)
		gradient = QRadialGradient(x + self._diameter / 2, y + self._diameter / 2,
			self._diameter * 0.4, self._diameter * 0.4, self._diameter * 0.4)
		gradient.setColorAt(0, Qt.GlobalColor.white)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		if self._led:
			gradient.setColorAt(1, on_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(on_color)
			# Draws the ellipse positioned at center with radii rx and ry.
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)
		else:
			gradient.setColorAt(1, off_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(off_color)
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)

	def setLed(self, val):
		self._led = val
		self.update()

	def getLed(self):
		self.update()
		return self._led

	led = pyqtProperty(bool, getLed, setLed)

