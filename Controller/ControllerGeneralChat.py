from Modules.FuncionesIA import FuncionesIA
from EduGeneralApp.models import General_Collection
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
import os

# Cargando variables de entorno
load_dotenv(override=True)

class GeneralChat:
    def __init__(self) -> None:
        self.funcionesIA = FuncionesIA()
    async def GeneralChat(self, message):
        '''
            cargar la clase del modulo (modelGeneral)
            Llamando la funcion principal para obtener la respuesta (mainFun)
        '''
        respuesta = await self.ResponseGeneralChat(message=message)
        return respuesta

    async def ResponseGeneralChat(self, message):
        '''
            Aqui se hara la logica para la respuesta de Ollama, importando los modulos de IA y de LLM

            pasos:
                1. Convertir el masaje de texto en un embedding para obtener el contexto con base a la similitd de la informacion de la base de datos de vectorial (Chroma)
                2. Con la informacion de la base de datos de vectorial (Chroma) llamar a la funcion de llamada de ollama para obtener la respuesta, con base al contexto obtenido en el paso anterior
                3. Si el contexto es un error, se devuelve el error

            pd: el nombre de la coleccion previamente se debe crear con la informacion que tiene la DB principal, consultar el Swagger para crear la coleccion
        '''
        try:
            #obtener el nombre de la coleccion que tiene la informacion de la base de datos de vectorial (Chroma)
            instancia = await sync_to_async(list)(General_Collection.objects.all())
            nameCollection = instancia[0].Nombre_Coleccion
            contexto_dict = await self.funcionesIA._get_context(userMessage=message, nameCollection=nameCollection)
            contexto = contexto_dict[0].get('content')
            responseGenerate = await self.funcionesIA._callGenerate(message_user=message, contextEmbedding=contexto)
            if 'error' in contexto_dict:
                return ({'error': contexto_dict['error']})
            elif 'error' in responseGenerate:
                return ({'error': responseGenerate['error']})
            else:
                respuesta = {
                    'response': responseGenerate,
                    'referencia': contexto_dict[0].get('url')
                }
                return respuesta
        except Exception as e:
            return {"error": f"{str(e)}"}
