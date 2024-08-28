from Modules.GeneralModel import GeneralModel
from Modules.ConfigDBModel import ModelDB
from Modules.AsistModel import AsistModel
from dotenv import load_dotenv
import os

# Cargando variables de entorno
load_dotenv(override=True)

class ControllerEduIA:
    def __init__(self, EngineAV=None, EngineChat=None):
        self.EngineAV = EngineAV
        self.EngineChat = EngineChat

    async def edulaAV(self, message):
        '''
            cargar la clase del modulo (modelAV)
            Llamando la funcion principal para obtener la respuesta (mainFun)
        '''
        modelAV = AsistModel()
        mainFun = await modelAV.responseAV(userMessage=message)
        return mainFun

    async def edulaGeneral(self, message):
        # Cargar clase con parámetros necesarios
        modelGeneral = GeneralModel()
        fun_model = await modelGeneral.responseGeneral(message_user=message)
        return fun_model

    async def main_engine(self, message):
        if self.EngineAV:
            return await self.edulaAV(message)
        elif self.EngineChat:
            return await self.edulaGeneral(message)
        else:
            return "Motor no encontrado"

class ControllerDataBase:
    def createDatabase(self, nameCollection, dataContent):
        try:
            objCollectionDB = ModelDB()
            createCollection = objCollectionDB.embeddingsDataBase(nameCollection=nameCollection, dataContext=dataContent)
            if createCollection:
                return {"success": "Colleccion creada"}
            else:
                return {'error': 'Error al crear la colleccion'}
        except Exception as e:
            return {'Exception error': f'Ocurrió un error al crear la colleccion: {str(e)}'}