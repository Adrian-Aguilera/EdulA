import Modules.FuncionesIA as FuncionesIA
from EduAssistApp.models import AssistantCollection
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
import os
load_dotenv(override=True)

class ControllerAsistenteChat:
    def __init__(self):
        self.FuncionesIA = FuncionesIA.FuncionesIA()

    async def main_engine(self, message):
        '''
            llamada a la funcion main_engine de la clase FuncionesIA
            llamada a la funcion _callChatGenerate de la clase FuncionesIA
        '''
        mainFun = await self.FuncionesIA._callChatGenerate(message)
        return mainFun

    async def ResponseAsistenteChat(self, message):
        '''
            llamada a la funcion main_engine de la clase FuncionesIA
            llamada a la funcion _callChatGenerate de la clase FuncionesIA
        '''
        try:
            instancia = await sync_to_async(list)(AssistantCollection.objects.all())
            nameCollection = instancia[0].Nombre_Coleccion
            EmbeddingsData = await self.FuncionesIA._responseEmbedding(userMessage=message, nameCollection=nameCollection)
            responseGenerate = await self.FuncionesIA._callChatGenerate(message_user=message, contextEmbedding=EmbeddingsData)
            if 'error' in EmbeddingsData:
                return ({'error': EmbeddingsData['error']})
            elif 'error' in responseGenerate:
                return ({'error': responseGenerate['error']})
            else:
                return ({'response': responseGenerate})
        except Exception as e:
            return {"error": f"{str(e)}"}