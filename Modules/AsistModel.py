from EduAssistApp.models import AssistantCollection
from asgiref.sync import async_to_sync, sync_to_async
from Modules.FuncionesIA import FuncionesIA

class AsistModel:
    async def responseAV(self, userMessage):
        try:
            instancia = await sync_to_async(list)(AssistantCollection.objects.all())
            nameCollection = instancia[0].Nombre_Coleccion
            EmbeddingsData = await FuncionesIA._get_context(userMessage=userMessage, nameCollection=nameCollection)
            responseGenerate = await FuncionesIA._callGenerate(message_user=userMessage, contextEmbedding=EmbeddingsData)
            if 'error' in EmbeddingsData:
                return ({'error': EmbeddingsData['error']})
            elif 'error' in responseGenerate:
                return ({'error': responseGenerate['error']})
            else:
                return ({'response': responseGenerate})
        except Exception as e:
            return {"error": f"{str(e)}"}