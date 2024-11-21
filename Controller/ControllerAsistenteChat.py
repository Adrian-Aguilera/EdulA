import Modules.FuncionesIA as FuncionesIA
from EduAssistApp.models import AssistantCollection
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
import os
load_dotenv(override=True)

class ControllerAsistenteChat:
    def __init__(self):
        self.FuncionesIA = FuncionesIA.FuncionesIA()

    async def AsistenteChat(self, conversacion):
        '''
            llamada a la funcion AsistenteChat que hace la la llamada a las funciones de la clase FuncionesIA
        '''
        respuestaChat = await self.ResponseAsistenteChat(conversacion)
        return respuestaChat

    async def ResponseAsistenteChat(self, conversacion):
        '''
            llamada a la funcion AsistenteChat de la clase FuncionesIA
            llamada a la funcion _callChatGenerate de la clase FuncionesIA, para formato de chat de la respuesta

            pd: el nombre de la coleccion previamente se debe crear con la informacion que tiene la DB principal, consultar el Swagger para crear la coleccion del asistente
            pd: toma el nombre de la coleccion del asistente
        '''
        try:
            instancia = await sync_to_async(list)(AssistantCollection.objects.all())
            nameCollection = instancia[0].Nombre_Coleccion
            print(f'conversacion desde el controllador asistente: {conversacion}')
            EmbeddingsData = await self.FuncionesIA._responseEmbedding(userMessage=conversacion, nameCollection=nameCollection)
            responseGenerate = await self.FuncionesIA._callChatGenerate(conversacion_Estudiante=conversacion, contextEmbedding=EmbeddingsData)
            if 'error' in EmbeddingsData:
                return ({'error': EmbeddingsData['error']})
            elif 'error' in responseGenerate:
                return ({'error': responseGenerate['error']})
            else:
                return ({'response': responseGenerate})
        except Exception as e:
            return {"error": f"{str(e)}"}