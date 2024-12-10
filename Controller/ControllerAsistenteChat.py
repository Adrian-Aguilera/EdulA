import Modules.FuncionesIA as FuncionesIA
from EduAsistenteApp.models import AssistantCollection
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
load_dotenv(override=True)

class ControllerAsistenteChat:
    def __init__(self):
        self.FuncionesIA = FuncionesIA.FuncionesIA()

    async def AsistenteChat(self, conversacion, historial):
        '''
            llamada a la funcion AsistenteChat que hace la la llamada a las funciones de la clase FuncionesIA
        '''
        respuestaChat = await self.ResponseAsistenteChat(pregunta=conversacion, historial=historial)
        return respuestaChat

    async def ResponseAsistenteChat(self, pregunta, historial:list):
        '''
            llamada a la funcion AsistenteChat de la clase FuncionesIA
            llamada a la funcion _callChatGenerate de la clase FuncionesIA, para formato de chat de la respuesta

            pd: el nombre de la coleccion previamente se debe crear con la informacion que tiene la DB principal, consultar el Swagger para crear la coleccion del asistente
            pd: toma el nombre de la coleccion del asistente
        '''
        try:
            # Obtener la colección del asistente
            instancia = await sync_to_async(list)(AssistantCollection.objects.all())
            if not instancia:
                return {"error": "No se encontró ninguna colección de asistente disponible."}

            nameCollection = instancia[0].Nombre_Coleccion

            print(f'pregunta a la cual se hara embedding: {pregunta}')
            # Obtener el contexto de embedding
            contexto_dict = await self.FuncionesIA._get_context(userMessage=pregunta, nameCollection=nameCollection)
            contexto = contexto_dict[0].get('content')
            # Añadir la pregunta al historial
            historial.append({"role": "user", "content": pregunta})
            # Llamar a la API para generar la respuesta del asistente
            respuestaChat = await self.FuncionesIA._callChatGenerate(historial=historial, contexto=contexto)
            url_referencia = contexto_dict[0].get('url')
            if 'error' in contexto_dict:
                return ({'errors': {
                    'error': contexto_dict['error'],
                    'mensaje': 'Error en el contexto del asistente'
                }})
            elif 'error' in respuestaChat:
                return ({'errors': {
                    'error': respuestaChat['error'],
                    'mensaje': 'Error en la respuesta del asistente'
                }})
            else:
                respuesta = {
                    'Edula-IA': respuestaChat,
                    'referencia': url_referencia
                }
                return respuesta
        except Exception as e:
            return {"error chat": f"{str(e)}"}