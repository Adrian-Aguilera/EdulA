from .GeneralModel import GeneralModel
from EduAssistApp.models import AssistantCollection
from asgiref.sync import async_to_sync, sync_to_async

class AsistModel:
    async def responseAV(self, userMessage):
        instancia = await sync_to_async(list)(AssistantCollection.objects.all())
        nameCollection = instancia[0].nameCollection
        responseAV = nameCollection
        return responseAV