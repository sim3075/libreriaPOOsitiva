import  sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QAbstractItemView, QInputDialog
from PyQt5 import uic, QtCore
from mundo import *




class LibreriaPoo(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/MainWindowLibreriaPoo.ui", self)
        self.setFixedSize(self.size())
        self.dialogo_agregar_ejemplar = DialogoAgregarEjemplar()
        self.dialogo_agregar_usuario = DialogoAgregarUsuario()
        self.libreria = Biblioteca()
        self.__configurar()
        self.__cargar_datos()
        self.__cargar_datos_usuario()




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
        self.Btn_dos.clicked.connect(self.pagina_usuario)
        self.btn_Agregar_catalogo.clicked.connect(self.abrir_dialogo_agregar_ejemplar)
        self.btn_Agregar_bolsa.clicked.connect(self.agregar_ejemplar_bolsa)
        self.Btn_eliminarEjemplar_Bolsa.clicked.connect(self.eliminar_item_bolsa)
        self.btn_registrar_usuario.clicked.connect(self.abrir_dialogo_agregar_usuario)


        #Cofiguracion QListView
        self.listView_ejemplares.setModel(QStandardItemModel())
        self.listView_usuarios.setModel(QStandardItemModel())


    def __cargar_datos(self):
        libros = list(self.libreria.catalogo.values())
        for libro in libros:
            item = QStandardItem(str(libro))
            item.libro = libro
            item.setEditable(False)
            self.listView_ejemplares.model().appendRow(item)

    def __cargar_datos_usuario(self):
        usuarios = list(self.libreria.usuarios.values())
        for usuario in usuarios:
            item = QStandardItem(str(usuario))
            item.usuario = usuario
            item.setEditable(False)
            self.listView_usuarios.model().appendRow(item)


    def agregar_ejemplar_bolsa(self):
        cantidad, ok_pressed = QInputDialog.getInt(self, "Agregar ejemplar al la bolsa", "Cantidad", 1)
        if ok_pressed:
            model = self.listView_ejemplares.model()
            value = model.itemFromIndex(self.listView_ejemplares.selectedIndexes()[0])
            item = self.libreria.agregar_ejemplar_bolsa(value.libro, cantidad)
            self.agregar_item_tabla(item)
            self.actualizar_total()

    def agregar_item_tabla(self, item):
        sub_total = "${:,.2f}".format(item.calcular_subtotal())
        celda_1 = QStandardItem(item.libro.titulo)
        celda_2 = QStandardItem(str(item.cantidad))
        celda_3 = QStandardItem(sub_total)
        celda_1.item = item
        model = self.tableView_bolsa.model()
        model.appendRow([celda_1, celda_2, celda_3])


    def eliminar_item_bolsa(self):
        selection_model = self.tableView_bolsa.selectionModel()
        model = self.tableView_bolsa.model()
        row_index = selection_model.selectedIndexes()[0].row()
        table_item = model.item(row_index)
        self.libreria.eliminar_ejemplar_bolsa(table_item.item.libro.scib)
        model.removeRow(row_index)
        self.actualizar_total()



    def actualizar_total(self):
        total = self.libreria.bolsa.calcular_total()
        self.lineEdit_total.setText("${:,.2f}".format(total))


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

    def abrir_dialogo_agregar_usuario(self):
        respuesta = self.dialogo_agregar_usuario.exec()
        if respuesta == QDialog.Accepted:
            dni = self.dialogo_agregar_usuario.le_dni.text()
            nombre = str(self.dialogo_agregar_usuario.le_nombre.text())
            try:
                usuario = self.libreria.registrar_usuario(dni, nombre)

            except DniExistenteError as error:
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
                model = self.listView_usuarios.model()
                item = QStandardItem(str(usuario))
                item.usuario = usuario
                item.setEditable(False)
                model.appendRow(item)
        self.dialogo_agregar_usuario.limpiar()

    def inicio(self):
        self.stackedWidget.setCurrentWidget(self.page)

    def pagina_listar_libro(self):
        self.stackedWidget.setCurrentWidget(self.page_uno)

    def pagina_usuario(self):
        self.stackedWidget.setCurrentWidget(self.page_dos)




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


class DialogoAgregarUsuario(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/Dialogo_AgregarUsuario.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):
        self.le_dni.setValidator(QRegExpValidator(QRegExp("\\d{10}"), self.le_dni))

    def limpiar(self):
        self.le_dni.clear()
        self.le_nombre.clear()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LibreriaPoo()
    win.show()
    sys.exit(app.exec())