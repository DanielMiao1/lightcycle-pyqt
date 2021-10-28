# -*- coding: utf-8 -*-

import random

from PyQt5.QtGui import *
from PyQt5.QtTest import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Text(QLabel):
	"""Override existing QLabel for color animation"""
	def __init__(self, parent, text=""):
		super().__init__(parent=parent)  # Initialize text
		self.text_color = None
		self.setText(text)  # Set text content

	def setColor(self, color):
		"""Color animation"""
		self.text_color = color  # Update color variable
		palette = self.palette()  # Create new palette
		palette.setColor(self.foregroundRole(), color)  # Set color for palette
		self.setPalette(palette)  # Set color of text to palette color

	color = pyqtProperty(QColor, fset=setColor)  # Define new PyQt Property for animation


class Button(QPushButton):
	"""Override existsing QPushButton for custom hover events"""
	def __init__(self, parent, text="", mouse_press_event=None):
		super().__init__(parent=parent)  # Initialize button
		self.letter_spacing = "2px"  # Set letter spacing variable
		self.background_color = None
		self.mouse_press_function = mouse_press_event
		self.setText(text)  # Set text content
		self.setFont(QFont("Impact", 15))  # Set text font
		self.setCursor(Qt.PointingHandCursor)
		self.setStyleSheet("background-color: white; border: none; letter-spacing: 2px;")  # Set QSS stylesheet attributes

	def enterEvent(self, event):
		"""Mouse hover in event"""
		self.letter_spacing = "3.5px"  # Change letter spacing
		super().enterEvent(event)

	def leaveEvent(self, event):
		"""Mouse hover out event"""
		self.letter_spacing = "2px"  # Revert letter spacing
		super().leaveEvent(event)

	def mousePressEvent(self, event):
		"""Mouse press event"""
		if self.mouse_press_function is not None:
			self.mouse_press_function()
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		"""Mouse release event"""
		super().mouseReleaseEvent(event)

	def setBackgroundColor(self, color: QColor):
		"""Background color animation"""
		self.background_color = color  # Update background color variable
		self.setStyleSheet(f"background-color: rgba{color.getRgb()}; border: none; letter-spacing: {self.letter_spacing};")  # Update stylesheet

	def setColor(self, color):
		"""Color animation"""
		self.text_color = color  # Update color variable
		palette = self.palette()  # Create new palette
		palette.setColor(self.foregroundRole(), color)  # Set color for palette
		self.setPalette(palette)  # Set color of text to palette color

	background = pyqtProperty(QColor, fset=setBackgroundColor)
	color = pyqtProperty(QColor, fset=setColor)


class Square(QPushButton):
	def __init__(self, parent, position, color):
		super().__init__(parent=parent)
		self.setStyleSheet(f"background-color: {color}; border: 0.5px solid black;")
		self.position = position
		self.color = color

	def update_(self):
		if self.parent().width() < self.parent().height():
			self.resize(QSize(self.parent().width() // 30, self.parent().width() // 30))
			self.move(QPoint(self.position[0] * (self.parent().width() // 30), self.position[1] * (self.parent().width() // 30)))
		else:
			self.resize(QSize(self.parent().height() // 30, self.parent().height() // 30))
			self.move(QPoint(self.position[0] * (self.parent().height() // 30), self.position[1] * (self.parent().height() // 30)))


class GameWindow(QWidget):
	"""30x30 point-board"""
	def __init__(self, parent):
		"""Setup widget"""
		super().__init__(parent=parent)  # Call superclass __init__

	def indexed(self):
		"""Initialization"""
		self.squares = []  # Define squares
		self.squares_group = QGroupBox(self)
		self.squares_group.resize(self.size())
		self.squares_group_layout = QGridLayout()
		for x in range(29):
			squares_row = []
			for y in range(29):
				squares_row.append(Square(self, [x, y], "#00002" + hex(random.randint(5, 15))[-1]))
				self.squares_group_layout.addWidget(squares_row[-1], x, y)
				squares_row[-1].update_()
			self.squares.append(squares_row)
		self.squares_group_layout.setSpacing(0)
		self.squares_group.setLayout(self.squares_group_layout)
		self.squares_group.show()
		QTest.qWait(250)
		self.update_()

	def update_(self):
		try:
			self.squares_group.resize(self.size())
			for x in self.squares:
				for y in x:
					y.update_()
			self.squares_group.move(QPoint((self.width() - self.squares[-1][-1].pos().x()) // 4, (self.height() - self.squares[-1][-1].pos().y()) // 4))
		except:
			pass

	def resizeEvent(self, event):
		self.update_()
		super().resizeEvent(event)


class MainWindow(QWidget):
	def __init__(self, parent):
		super().__init__(parent=parent)  # Initialize page
		self.resize_function = self.initialResize
		self.start_game = None
		# Title
		self.title = Text(self, "LightCycle")  # Add title
		self.title.setAlignment(Qt.AlignCenter)
		# Title animation
		self.title_animation = QPropertyAnimation(self.title, b"color")  # Create animation
		self.title_animation.setLoopCount(1)  # Set loop count
		self.title_animation.setDuration(15000)  # Set loop duration
		self.title_animation.setStartValue(QColor("#0000FF"))  # Set start color
		self.title_animation.setEndValue(QColor("#AA00FF"))  # Set end color
		self.title_animation.finished.connect(lambda: self.changeAnimationDirection(self.title_animation))  # Call lambda: sel... when animation finishes
		self.title_animation.start()  # Start animation
		self.title.show()  # Show title
		# Start button
		self.start_button = Button(self, "Start Game", mouse_press_event=self.start)
		# Start button animation
		self.button_animation = QPropertyAnimation(self.start_button, b"background")  # Create animation
		self.button_animation.setLoopCount(1)  # Set loop count
		self.button_animation.setDuration(45000)  # Set loop duration
		self.button_animation.setStartValue(QColor("#88FFFF"))  # Set start color
		self.button_animation.setEndValue(QColor("#5555FF"))  # Set end color
		self.button_animation.finished.connect(lambda: self.changeAnimationDirection(self.button_animation))  # Call function when animation finishes
		self.button_animation.start()  # Start animation
		self.start_button.show()  # Show start button

	def start(self):
		"""First phase of starting game"""
		# Fade objects
		# Title animation
		self.title_animation.stop()  # Stop existing title animation
		# Create new title text color animation
		self.title_animation = QPropertyAnimation(self.title, b"color")  # Create animation
		self.title_animation.setLoopCount(1)  # Set loop count
		self.title_animation.setDuration(500)  # Set loop duration
		self.title_animation.setStartValue(self.title.text_color)  # Set start color
		self.title_animation.setEndValue(QColor.fromRgb(*self.title.text_color.getRgb()[:-1], 0))  # Set end color
		self.title_animation.finished.connect(self.start1)  # Call self.start1 when animation finishes
		self.title_animation.start()  # Start animation
		# Start button animation
		self.button_animation.stop()  # Stop existing start button animation
		self.start_button.mouse_press_function = None
		# Create new start button background color animation
		self.button_animation = QPropertyAnimation(self.start_button, b"background")  # Create animation
		self.button_animation.setLoopCount(1)  # Set loop count
		self.button_animation.setDuration(500)  # Set loop duration
		self.button_animation.setStartValue(self.start_button.background_color)  # Set start color
		self.button_animation.setEndValue(QColor.fromRgb(*self.start_button.background_color.getRgb()[:-1], 0))  # Set end color
		self.button_animation.finished.connect(lambda: self.start_button.setCursor(Qt.ArrowCursor))
		self.button_animation.start()  # Start animation
		# Create new start button text color animation
		self.button_animation1 = QPropertyAnimation(self.start_button, b"color")  # Create animation
		self.button_animation1.setLoopCount(1)  # Set loop count
		self.button_animation1.setDuration(500)  # Set loop duration
		self.button_animation1.setStartValue(QColor("#000000"))  # Set start color
		self.button_animation1.setEndValue(QColor("transparent"))  # Set end color
		self.button_animation1.start()  # Start animation

	def start1(self):
		"""Second phase of starting game"""
		self.start_game()

	def changeAnimationDirection(self, animation):
		"""Invert animation direction"""
		animation.setDirection(int(not animation.direction()))  # Invert animation direction
		animation.start()  # Restart animation

	def onResize(self, event):
		"""Normal resize event"""
		# Title
		self.title.setFont(QFont("Impact", (event.size().width() + event.size().height()) // 24))  # Enlarge/shrink the title font size
		self.title.resize(QSize(event.size().width(), event.size().height() // 5))  # Resize title
		# Start button
		self.start_button.resize(QSize(event.size().width() // 5, event.size().height() // 10))  # Resize start button according to the new window size. This statement has to be before the button move statement (on the next line)
		self.start_button.move(QPoint((event.size().width() // 2) - (self.start_button.width() // 2), event.size().height() // 2))  # Move start button to center of screen

	def initialResize(self, event):
		"""First resize event"""
		self.resize_function = self.onResize  # Change resize function pointer
		# Window background color animation
		self.window_color_animation = QPropertyAnimation(self.parent().parent(), b"background")  # Create animation
		self.window_color_animation.setLoopCount(1)  # Set loop count
		self.window_color_animation.setDuration(1150)  # Set animation duration
		self.window_color_animation.setStartValue(QColor("#FFFFFF"))  # Set start value
		self.window_color_animation.setEndValue(QColor("#000000"))  # Set end value
		self.window_color_animation.start()  # Start animation
		# Title
		self.title.setFont(QFont("Impact", (event.size().width() + event.size().height()) // 24))  # Enlarge/shrink the title font size
		self.title.resize(QSize(event.size().width(), event.size().height() // 5))  # Resize title
		# Start button
		self.start_button.resize(QSize(event.size().width() // 5, event.size().height() // 10))  # Resize start button according to the new window size. This statement has to be before the button move statement (on the next line)
		self.start_button.move(QPoint(-self.start_button.width(), self.height() // 2))  # Move start button
		# Title animation
		self.title_slide_animation = QPropertyAnimation(self.title, b"pos")  # Create animation
		self.title_slide_animation.setLoopCount(1)  # Set loop count
		self.title_slide_animation.setDuration(750)  # Set animation duration
		self.title_slide_animation.setStartValue(QPoint(-self.title.width(), 0))  # Set start point
		self.title_slide_animation.setEndValue(QPoint(0, 0))  # Set end point
		self.title_slide_animation.finished.connect(self.startButtonAnimation)  # Start button animation when title slide animation is finished
		self.title_slide_animation.start()  # Start animation

	def startButtonAnimation(self):
		"""Start button slide-in animation"""
		self.start_button_animation = QPropertyAnimation(self.start_button, b"pos")  # Create animation
		self.start_button_animation.setLoopCount(1)  # Set loop count
		self.start_button_animation.setDuration(500)  # Set animation duration
		self.start_button_animation.setStartValue(QPoint(-self.start_button.width(), self.height() // 2))  # Set start point
		self.start_button_animation.setEndValue(QPoint((self.width() // 2) - (self.start_button.width() // 2), self.height() // 2))  # Set end point
		self.start_button_animation.start()  # Start animation

	def resizeEvent(self, event):
		"""Window resize event"""
		self.resize_function(event)
		super().resizeEvent(event)


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()  # Initialize window
		self.setMinimumSize(QSize(600, 600))  # Set window minimum size
		self.setWindowTitle("LightCycle")  # Set window title
		self.setStyleSheet("background-color: white;")  # Change background color
		self.stacked_pages = QStackedWidget(self)  # Add stacked widget
		self.pages = {
			"main": MainWindow(self),
			"game": GameWindow(self)
		}  # Add pages
		self.pages["main"].start_game = lambda: self.updateStackIndex(1, self.pages["game"])  # Update start_game attribute of MainWindow
		# Add pages to stacked widget
		self.stacked_pages.addWidget(self.pages["main"])
		self.stacked_pages.addWidget(self.pages["game"])
		self.stacked_pages.move(0, 0)  # Move pages
		self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		self.show()  # Show window

	def resizeEvent(self, event):
		"""Window resize event"""
		self.stacked_pages.resize(event.size())

	def updateStackIndex(self, index, widget):
		self.stacked_pages.setCurrentIndex(index)  # Update pages index
		# Try to call widget.indexed function
		try:
			widget.indexed()
		except:
			pass

	def setBackgroundColor(self, color: QColor):
		"""Background color animation"""
		self.background_color = color  # Update background color variable
		self.setStyleSheet(f"background-color: rgba{color.getRgb()};")  # Update stylesheet

	background = pyqtProperty(QColor, fset=setBackgroundColor)


application, window = QApplication([]), Window()  # Create new QApplication and instance of Window()
application.exec_()  # Execute application
