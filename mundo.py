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
        self.items.append(Item(libro, cantidad))

    def calcular_total(self):
        total = 0
        for item in self.items:
            total += item.calcular_subtotal()
            return total

    def quitar_item(self, scib):
        self.item = [item for item in self.items if item.scib != scib]
class Usuario:
    def __init__(self, dni: str, nombre: str):
        self.dni: str = dni
        self.nombre: str = nombre
        self.bolsa= Bolsa()



class Biblioteca:
    def __init__(self):
        self.bolsa = Bolsa()
        self.total_prestados = 0
        self.total_vendidos = 0
        self.total_devueltos= 0
        self.usuarios = {}
        self.libros = {}
        self.__cargar_catalogo()


    def __cargar_catalogo(self):
        with open("data/catalogo.csv") as file:
            csv_data = csv.reader(file, delimiter=":")
            libros = map(lambda data: Libro(data[0], data[1], int(data[2])), csv_data)
            self.catalogo = {lib.scib: lib for lib in libros}

    def adicionar_ejemplar_al_catalogo(self, scib, titulo, precio):
        if  scib == "" or titulo == "":
            raise  EspaciosVacios(f"Rellenar todos los campos")
        if scib not in self.libros.keys():
            ejemplar = Libro(scib, titulo, precio)
            self.libros[scib] = Libro(scib, titulo, precio)
            return ejemplar
        else:
            raise EjemplarExistenteError(f"Ya existe un libro con el scib {scib}", scib)


    def agregar_ejemplar_bolsa(self, scib, cantidad):
        if scib in self.catalogo.keys():
            self.bolsa.agregar_item(self.libros[scib], cantidad)

    def eliminar_libro(self, scib: str):
        self.libros.pop(scib)

    def cargar_libros(self):
        self.libros["216676"]=Libro("216676",
                                    "código limpio",
                                    85000)

        self.libros["786534"]=Libro("786534",
                                    "lenguajes II",
                                    32000)

        self.libros["396784"]=Libro("396784",
                                    "fundamentos de programación",
                                    56000)

    def buscar_libro(self, scib: str):
       if scib in self.libros.keys():
           return self.libros[scib]
       else:
           return None

    def registrar_usuario(self, dni: str, nombre: str):
        if self.buscar_usuario(dni) is None:
            usuario = Usuario(dni, nombre)
            self.usuarios[dni] = usuario
            return True
        else:
            return False

    def buscar_usuario(self, dni: str)-> Optional[Usuario]:
        if dni in self.usuarios.keys():
            return self.usuarios[dni]
        else:
            return None



class Prestado:


    def __init__(self, scib: int, dia: int, mes: str):
        self.scib= scib
        self.dia= dia
        self.mes= mes
        self.prestados={}

    def agregar_a_prestados(self, dni:str, scib: str):
        self.prestados[dni]= Biblioteca

