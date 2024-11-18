from Modules.GeneralModel import GeneralModel
from dotenv import load_dotenv
import os

# Cargando variables de entorno
load_dotenv(override=True)

class GeneralChat:
    async def GeneralChat(self, message):
        '''
            cargar la clase del modulo (modelGeneral)
            Llamando la funcion principal para obtener la respuesta (mainFun)
        '''
        modelGeneral = GeneralModel()
        mainFun = await modelGeneral.responseGeneral(message_user=message)
        return mainFun