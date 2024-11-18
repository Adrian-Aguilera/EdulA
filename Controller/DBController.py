from Modules.ConfigDBModel import ModelDB

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