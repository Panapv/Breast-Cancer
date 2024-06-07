from pyspark.sql import SparkSession
import os
# import kaggle

class HandlerBranchCode:

    # Create a SparkSession
    @staticmethod
    def newSession(name):
        spark = SparkSession.builder \
            .appName(name) \
            .getOrCreate()
        return spark

    # Crear carpetas por año, mes y día
    @staticmethod
    def partition_folder(RUTA):
        # Comprobamos que existan las particiones
        path = os.path.join(str(RUTA))
        os.makedirs(path, exist_ok=True)
        return path

    # Guardamos el fichero en su carpeta correspondiente
    @staticmethod
    def clean_data(RUTA_OG, RUTA_DEST):
        spark = HandlerBranchCode.newSession('New Session')

        data = spark.read.csv(RUTA_OG, header=True, inferSchema=True)
        ruta_destino = os.path.join(RUTA_DEST, f'breast_cancer')

        data.write.json(ruta_destino)

        spark.stop()

    @staticmethod
    def transform_data(RUTA_OG, RUTA_DEST):
        return 0

    # @staticmethod
    # def get_kaggle():
    #     dataset_name = 'alphiree/cardiovascular-diseases-risk-prediction-dataset'
    #     download_path = './raw'
    #     kaggle.api.dataset_download_files(dataset_name, download_path, unzip=True)
    #     og_name =  './raw/'+os.listdir('./raw')[0]
    #     os.rename(og_name, './raw/cardio.csv')


path_staging = HandlerBranchCode.partition_folder('.\\staging')
HandlerBranchCode.clean_data('.\\raw\\breast_cancer.csv', path_staging)

path_business = HandlerBranchCode.partition_folder('.\\business')
HandlerBranchCode.clean_data('.\\staging\\breast_cancer', path_business)