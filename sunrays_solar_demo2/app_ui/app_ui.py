import sys

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QDesktopWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('My App')
        self.setGeometry(300, 300, 400, 300)

        self.setIcon()
        self.setIconModes()
        self.setAppCenter()
        self.setButton()
        self.setAboutButton()

    # set icon
    def setIcon(self):
        appIcon = QIcon("../401262_archlinux_icon.png")
        self.setWindowIcon(appIcon)

    # set icon
    def setIconModes(self):
        icon1 = QIcon('../401262_archlinux_icon.png')
        label1 = QLabel('simple', self)
        pixmap1 = icon1.pixmap(50, 50, QIcon.Active, QIcon.On)
        label1.setPixmap(pixmap1)
        label1.move(10, 10)
        label1.setToolTip('Active')

    # set app in center
    def setAppCenter(self):
        frame = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())

    # set quit button
    def setButton(self):
        self.btn1 = QPushButton('Quit', self)
        self.btn1.move(110, 250)
        self.btn1.clicked.connect(self.quitApp)

    # set quit button
    def quitApp(self):
        app_quit = QMessageBox.question(self, 'Conformation', 'Do you want to clos this app',
                                        QMessageBox.Yes, QMessageBox.No)
        if app_quit == QMessageBox.Yes:
            myApp.quit()
        elif app_quit == QMessageBox.No:
            pass

    # set about button
    def setAboutButton(self):
        self.btn1 = QPushButton('About Box', self)
        self.btn1.move(110, 220)
        self.btn1.clicked.connect(self.aboutBox)

    # set quit button
    def aboutBox(self):
        QMessageBox.about(self.btn1, 'About Software', 'This is a sun rays quotation software')


myApp = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(myApp.exec_())
