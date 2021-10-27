# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Text(QLabel):
	"""Override existing QLabel for color animation"""
	def __init__(self, parent, text=""):
		super().__init__(parent=parent)  # Initialize text
		self.setText(text)  # Set text content

	def setColor(self, color):
		"""Color animation"""
		palette = self.palette()  # Create new palette
		palette.setColor(self.foregroundRole(), color)  # Set color for palette
		self.setPalette(palette)  # Set color of text to palette color

	color = pyqtProperty(QColor, fset=setColor)  # Define new PyQt Property for animation


class Button(QPushButton):
	"""Override existsing QPushButton for custom hover events"""
	def __init__(self, parent, text=""):
		super().__init__(parent=parent)  # Initialize button
		self.letter_spacing = "2px"  # Set letter spacing variable
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
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		"""Mouse release event"""
		super().mouseReleaseEvent(event)

	def setBackgroundColor(self, color: QColor):
		"""Background color animation"""
		self.setStyleSheet(f"background-color: rgba{color.getRgb()}; border: none; letter-spacing: {self.letter_spacing};")

	background = pyqtProperty(QColor, fset=setBackgroundColor)


class GameWindow(QWidget):
	def __init__(self, parent):
		super().__init__(parent=parent)  # Initialize page


class MainWindow(QWidget):
	def __init__(self, parent):
		super().__init__(parent=parent)  # Initialize page
		# Title
		self.title = Text(self, "LightCycle")  # Add title
		self.title.setAlignment(Qt.AlignCenter)  # Set title alignment
		# Title animation
		self.title_animation = QPropertyAnimation(self.title, b"color")  # Create animation
		self.title_animation.setLoopCount(1)  # Set loop count
		self.title_animation.setDuration(15000)  # Set loop duration
		self.title_animation.setStartValue(QColor("#0000FF"))  # Set start color
		self.title_animation.setEndValue(QColor("#AA00FF"))  # Set end color
		self.title_animation.finished.connect(lambda: self.changeAnimationDirection(self.title_animation))  # Call lambda: sel... when animation finishes
		self.title_animation.start()  # Start animation
		# Start button
		self.start_button = Button(self, "Start Game")
		# Start button animation
		self.button_animation = QPropertyAnimation(self.start_button, b"background")  # Create animation
		self.button_animation.setLoopCount(1)  # Set loop count
		self.button_animation.setDuration(45000)  # Set loop duration
		self.button_animation.setStartValue(QColor("#88FFFF"))  # Set start color
		self.button_animation.setEndValue(QColor("#0000FF"))  # Set end color
		self.button_animation.finished.connect(lambda: self.changeAnimationDirection(self.button_animation))  # Call function when animation finishes
		self.button_animation.start()  # Start animation

	def changeAnimationDirection(self, animation):
		animation.setDirection(int(not animation.direction()))  # Invert animation direction
		animation.start()  # Restart animation

	def resizeEvent(self, event):
		"""Window resize event"""
		# Title
		self.title.setFont(QFont("Impact", event.size().width() // 12))  # Enlarge/shrink the title font size
		self.title.resize(QSize(event.size().width(), event.size().height() // 5))  # Resize title
		# Start button
		self.start_button.resize(QSize(event.size().width() // 7, event.size().height() // 10))  # Resize start button according to the new window size. This statement has to be before the button move statement (on the next line)
		self.start_button.move(QPoint((event.size().width() // 2) - (self.start_button.width() // 2), event.size().height() // 2))  # Move start button to center of screen
		super().resizeEvent(event)


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()  # Initialize window
		self.setMinimumSize(QSize(1080, 720))  # Set window minimum size
		self.setWindowTitle("LightCycle")  # Set window title
		self.setStyleSheet("background-color: white;")  # Change background color
		self.stacked_pages = QStackedWidget(self)  # Add stacked widget
		self.pages = {
			"main": MainWindow(self),
			"game": GameWindow(self)
		}  # Add pages
		# Add pages to stacked widget
		self.stacked_pages.addWidget(self.pages["main"])
		self.stacked_pages.addWidget(self.pages["game"])
		self.stacked_pages.move(0, 0)  # Move pages
		self.show()  # Show window

	def resizeEvent(self, event):
		"""Window resize event"""
		self.stacked_pages.resize(event.size())


application, window = QApplication([]), Window()  # Create new QApplication and instance of Window()
application.exec_()  # Execute application
