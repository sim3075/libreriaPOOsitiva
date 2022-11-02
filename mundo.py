from typing import Optional
from excepciones import  *
import csv

class Libro:

    def __init__(self, scib:str, titulo: str, precio: int):
        self.scib= scib
        self.titulo= titulo
        self.precio = precio

    def __str__(self):
        return f"CODIGO: {self.scib}//TITULO: {self.titulo}//$PRECIO: {self.precio}"

class Item:
    def __init__(self, libro, cantidad):
        self.libro = libro
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.libro.precio * self.cantidad


class Bolsa:
    def __init__(self):
        self.items = []

    def agregar_item(self, libro, cantidad):
        item = Item(libro, cantidad)
        self.items.append(Item(libro, cantidad))
        return  item

    def calcular_total(self):
        total = 0
        for item in self.items:
            total += item.calcular_subtotal()
        return total

    def quitar_item(self, scib):
        self.item = [item for item in self.items if item.libro.scib != scib]
class Usuario:
    def __init__(self, dni: str, nombre: str):
        self.dni: str = dni
        self.nombre: str = nombre


    def __str__(self):
        return f"DNI: {self.dni}---NOMBRE: {self.nombre}"
class Prestado:
    def __init__(self):
        self.prestados=[]

    def agregar_item(self, dni, nombre):
        item = Usuario(dni, nombre)
        self.prestados.append(Usuario(dni, nombre))
        return  item

    def calcular_total(self):
        total = 0
        for item in self.prestados:
            total += item.calcular_subtotal()
        return total

    def quitar_item(self, dni):
        self.item = [item for item in self.prestados if item.libro.scib != dni]




class Biblioteca:
    def __init__(self):
        self.bolsa = Bolsa()
        self.libros = {}
        self.__cargar_catalogo()
        self.__cargar_usuarios()
        self.prestamo = Prestado()


    def __cargar_catalogo(self):
        with open("data/catalogo.csv") as file:
            csv_data = csv.reader(file, delimiter=":")
            libros = map(lambda data: Libro(data[0], data[1], int(data[2])), csv_data)
            self.catalogo = {lib.scib: lib for lib in libros}


    def __cargar_usuarios(self):
        with open("data/usuarios.csv") as usuario:
            csvData = csv.reader(usuario, delimiter=":")
            usuarios = map(lambda data: Usuario(data[0], data[1]), csvData)
            self.usuarios = {usuario.dni: usuario for usuario in usuarios}


    def registrar_usuario(self, dni, nombre):
        if  dni == "" or nombre == "":
            raise  EspaciosVacios(f"Rellenar todos los campos")
        if dni not in self.usuarios.keys():
            usuario = Usuario(dni, nombre)
            self.usuarios[dni] = Usuario(dni, nombre)
            return usuario
        else:
            raise DniExistenteError(f"Ya existe un libro con el scib {dni}", dni)

    def adicionar_ejemplar_al_catalogo(self, scib, titulo, precio):
        if  scib == "" or titulo == "":
            raise  EspaciosVacios(f"Rellenar todos los campos")
        if scib not in self.libros.keys():
            ejemplar = Libro(scib, titulo, precio)
            self.libros[scib] = Libro(scib, titulo, precio)
            return ejemplar
        else:
            raise EjemplarExistenteError(f"Ya existe un libro con el scib {scib}", scib)


    def agregar_ejemplar_bolsa(self, libro, cantidad):
        return self.bolsa.agregar_item(libro, cantidad)



    def eliminar_ejemplar_bolsa(self, scib):
        self.bolsa.quitar_item(scib)

    # def cargar_libros(self):
    #     self.libros["216676"]=Libro("216676",
    #                                 "código limpio",
    #                                 85000)
    #
    #     self.libros["786534"]=Libro("786534",
    #                                 "lenguajes II",
    #                                 32000)
    #
    #     self.libros["396784"]=Libro("396784",
    #                                 "fundamentos de programación",
    #                                 56000)
    #
    #
    #
    # def registrar_usuario(self, dni: str, nombre: str):
    #     if self.buscar_usuario(dni) is None:
    #         usuario = Usuario(dni, nombre)
    #         self.usuarios[dni] = usuario
    #         return True
    #     else:
    #         return False
    #
    # def buscar_usuario(self, dni: str)-> Optional[Usuario]:
    #     if dni in self.usuarios.keys():
    #         return self.usuarios[dni]
    #     else:
    #         return None




    def agregar_a_prestados(self, prestamo, nombre):
        self.prestamo.agregar_item(prestamo, nombre)


