import  sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import  uic
from mundo import *


class LibreriaPoo(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/MainWindowLibreriaPoo.ui", self)
        self.setFixedSize(self.size())
        self.libreria = Biblioteca()

    def __configurar(self):
        self.listview_libros.setModel(QStandardItemModel())

    def __cargar_datos(self):
        libros = list(self.libreria.caatalogo.values())
        for libro in libros:
            item = QStandardItem(str(libro))
            item.libro = libro
            item.setEditable(False)
            self.listview_libros.model().appendRow(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LibreriaPoo()
    win.show()
    sys.exit(app.exec())