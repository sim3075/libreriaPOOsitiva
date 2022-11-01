import  sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QAbstractItemView, QInputDialog
from PyQt5 import  uic
from mundo import *




class LibreriaPoo(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/MainWindowLibreriaPoo.ui", self)
        self.setFixedSize(self.size())
        self.dialogo_agregar_ejemplar = DialogoAgregarEjemplar()
        self.libreria = Biblioteca()
        self.__configurar()
        self.__cargar_datos()




    def __configurar(self):
        #Configuracion Table View
        table_model = QStandardItemModel()
        table_model.setHorizontalHeaderLabels(["Ejemplar", "Cant.", "Subtotal"])
        self.tableView_bolsa.setModel(table_model)
        self.tableView_bolsa.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_bolsa.setColumnWidth(0, 230)
        self.tableView_bolsa.setColumnWidth(1, 65)
        self.tableView_bolsa.setColumnWidth(2, 150)

        #Configuracion Botones
        self.btn_inicio.clicked.connect(self.inicio)
        self.Btn_uno.clicked.connect(self.pagina_listar_libro)
        self.btn_Agregar_catalogo.clicked.connect(self.abrir_dialogo_agregar_ejemplar)
        self.btn_Agregar_bolsa.clicked.connect(self.agregar_ejemplar_bolsa)

        #Cofiguracion QListView
        self.listView_ejemplares.setModel(QStandardItemModel())


    def __cargar_datos(self):
        libros = list(self.libreria.catalogo.values())
        for libro in libros:
            item = QStandardItem(str(libro))
            item.libro = libro
            item.setEditable(False)
            self.listView_ejemplares.model().appendRow(item)


    def agregar_ejemplar_bolsa(self):
        cantidad, ok_pressed = QInputDialog.getInt(self, "Agregar ejemplar al la bolsa", "Cantidad", 1)
        if ok_pressed:
            model = self.listView_ejemplares.model()
            value = model.itemFromIndex(self.listview.selectedIndexes()[0])

    def abrir_dialogo_agregar_ejemplar(self):
        respuesta = self.dialogo_agregar_ejemplar.exec()
        if respuesta == QDialog.Accepted:
            scib = self.dialogo_agregar_ejemplar.le_scib.text()
            titulo = self.dialogo_agregar_ejemplar.le_titulo.text()
            precio = self.dialogo_agregar_ejemplar.le_precio.text()
            try:
                libro = self.libreria.adicionar_ejemplar_al_catalogo(scib, titulo, precio)

            except EjemplarExistenteError as error:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Error")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText(error.mensaje)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()

            except EspaciosVacios as error:
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Error")
                    msg_box.setIcon(QMessageBox.Critical)
                    msg_box.setText(error.mensaje)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec()
            else:
                model = self.listView_ejemplares.model()
                item = QStandardItem(str(libro))
                item.libro = libro
                item.setEditable(False)
                model.appendRow(item)
        self.dialogo_agregar_ejemplar.limpiar()

    def inicio(self):
        self.stackedWidget.setCurrentWidget(self.page)

    def pagina_listar_libro(self):
        self.stackedWidget.setCurrentWidget(self.page_uno)




class DialogoAgregarEjemplar(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/Dialogo_AgregarEjemplar.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):
        self.le_scib.setValidator(QRegExpValidator(QRegExp("\\d{6}"), self.le_scib))
        self.le_precio.setValidator(QDoubleValidator(0, 9999999, 2, self.le_precio))


    def limpiar(self):
        self.le_scib.clear()
        self.le_precio.clear()
        self.le_titulo.clear()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LibreriaPoo()
    win.show()
    sys.exit(app.exec())