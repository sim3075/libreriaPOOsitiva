class LibreriaError(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje

class EjemplarExistenteError(LibreriaError):

    def __init__(self, mensaje, scib):
        super().__init__(mensaje)
        self.scib = scib

class EspaciosVacios(LibreriaError):
    def __init__(self, mensaje):
        super().__init__(mensaje)