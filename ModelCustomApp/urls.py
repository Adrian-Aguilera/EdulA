from django.urls import path
from .views import CustomModel
urlpatterns = [
    path('Model/create', CustomModel.createModelCustom, name="modelCustom"),
    path('Model/show', CustomModel.showAllModel, name="show all model"),
    path('Model/SearchAvailable', CustomModel.searchModelCustom, name="Model Available"),
    path('Model/ollmaClient', CustomModel.ConnectOllama, name='ollamaClient'),
    path('Model/delete', CustomModel.deleteModel, name='Modelo usado en la eliminacion de modelos existentes')
]