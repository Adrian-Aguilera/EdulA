from Modules.ConfigDBModel import ModelDB, ModelDBRag
from asgiref.sync import async_to_sync

class ControllerDataBase:
    def createDatabase(self, nameCollection, dataContent):
        try:
            objCollectionDB = ModelDB()
            createCollection = objCollectionDB.embeddingsDataBase(nameCollection=nameCollection, dataContext=dataContent)
            if createCollection:
                return {"success": "Colleccion Embedding creada Exitosamente"}
            else:
                return {'error': 'Error al crear la colleccion'}
        except Exception as e:
            return {'Exception error': f'Ocurrió un error al crear la colleccion: {str(e)}'}

    def createCollection(self, documentos, nombre_Coleccion):
        try:
            objeto = ModelDBRag()
            crear_Coleccion = async_to_sync()(objeto.CargarDocumentos)(nombre_Coleccion=nombre_Coleccion, documentos=documentos)
            print(f'crear_Coleccion: {crear_Coleccion}')
            if crear_Coleccion.get('success'):
                return {"success": "Colleccion Embedding creada Exitosamente"}
            else:
                return {'error': crear_Coleccion}
        except Exception as e:
            return {'Collection error': f' {str(e)}'}