from .GeneralModel import GeneralModel
from EduAssistApp.models import AssistantCollection
from asgiref.sync import async_to_sync, sync_to_async
from Modules.GeneralModel import GeneralModel

class AsistModel:
    async def responseAV(self, userMessage):
        try:
            instancia = await sync_to_async(list)(AssistantCollection.objects.all())
            nameCollection = instancia[0].nameCollection
            EmbeddingsData = await GeneralModel._responseEmbedding(userMessage=userMessage, nameCollection=nameCollection)
            responseGenerate = await GeneralModel._callGenerate(message_user=userMessage, contextEmbedding=EmbeddingsData)
            if 'error' in EmbeddingsData:
                return ({'error': EmbeddingsData['error']})
            elif 'error' in responseGenerate:
                return ({'error': responseGenerate['error']})
            else:
                return ({'response': responseGenerate})
        except Exception as e:
            return {"error": f"{str(e)}"}