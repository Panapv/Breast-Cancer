from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import when
import os
# import kaggle

class HandlerBranchCode:

    # Create a SparkSession
    @staticmethod
    def newSession(name):
        print('Creando nueva sesión...')
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
    def clean_data(RUTA_OG, RUTA_DEST, SPARK):
        print('Pasando a la capa Staging...')
        spark = SPARK

        data = spark.read.csv(RUTA_OG, header=True, inferSchema=True)
        ruta_destino = os.path.join(RUTA_DEST, f'breast_cancer')

        data.write.parquet(ruta_destino)

    @staticmethod
    def transform_data(RUTA_OG, RUTA_DEST, SPARK):
        print('Pasando a la capa Business...')
        spark = SPARK

        data = spark.read.parquet(RUTA_OG)
        ruta_destino = os.path.join(RUTA_DEST, f'breast_cancer')

        #transformaciones

        data = data.withColumn('diagnosis' , when(data['diagnosis'] == 'M', 'Maligno').when(data['diagnosis'] == 'B', 'Benigno').otherwise(data['diagnosis']))

        old_cols = ["diagnosis","radius_mean","texture_mean","perimeter_mean","area_mean","smoothness_mean","compactness_mean","concavity_mean","concave points_mean","symmetry_mean","fractal_dimension_mean","radius_se","texture_se","perimeter_se","area_se","smoothness_se","compactness_se","concavity_se","concave points_se","symmetry_se","fractal_dimension_se","radius_worst","texture_worst","perimeter_worst","area_worst","smoothness_worst","compactness_worst","concavity_worst","concave points_worst","symmetry_worst","fractal_dimension_worst"]
        new_cols = ["Diagnóstico","Radio medio","Textura media","Perímetro medio","Área media","Suavidad media","Compacidad media","Concavidad media","Puntos cóncavos medios","Simetría media","Dimensión fractal media","Error estándar del radio","Error estándar de la textura","Error estándar del perímetro","Error estándar del área","Error estándar de la suavidad","Error estándar de la compacidad","Error estándar de la concavidad","Error estándar de los puntos cóncavos","Error estándar de la simetría","Error estándar de la dimensión fractal","Peor radio","Peor textura","Peor perímetro","Peor área","Peor suavidad","Peor compacidad","Peor concavidad","Peor puntuación de los puntos cóncavos","Peor simetría","Peor dimensión fractal"]
        data = data.select([col(old_col).alias(new_col) for old_col, new_col in zip(old_cols, new_cols)])

        data.write.parquet(ruta_destino)

    # @staticmethod
    # def get_kaggle():
    #     print('Pasando a la capa raw...')
    #     dataset_name = 'alphiree/cardiovascular-diseases-risk-prediction-dataset'
    #     download_path = './raw'
    #     kaggle.api.dataset_download_files(dataset_name, download_path, unzip=True)
    #     og_name =  './raw/'+os.listdir('./raw')[0]
    #     os.rename(og_name, './raw/cardio.csv')