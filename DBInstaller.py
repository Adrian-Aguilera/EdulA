import os
import sys

'''
Crear una carpeta para la base de datos
'''

def createDBFolder():
    try:
        os.mkdir("DB")
        print("Carpeta creada - >_<")
    except FileExistsError:
        print("Carpeta ya existe - X_X!")

if __name__ == "__main__":
    createDBFolder()