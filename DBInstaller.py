import os
import sys

'''
Crear una carpeta para la base de datos
'''

def createDBFolder():
    try:
        os.mkdir("DB")
        print("Carpeta creada")
    except FileExistsError:
        print("Carpeta ya existe")

if __name__ == "__main__":
    createDBFolder()