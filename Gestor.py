import xml.etree.ElementTree as ET

class Gestor:
    def __init__(self):
        self.cargado = False
        
    def limpiar(self):
        self.cargado = False
        
    def leer_archivo(self, ruta_entrada): # Leer el archivo con Element Tree
       pass