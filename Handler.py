from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import when
import os
import kaggle

class HandlerBranchCode:

    # Create a SparkSession
    @staticmethod
    def newSession(name):
        # Crear la sesión Spark sin imprimir el mensaje de advertencia
        spark = SparkSession.builder \
            .appName(name) \
            .getOrCreate()
    
        # Ajustar el nivel de registro a ERROR para eliminar el warning
        spark.sparkContext.setLogLevel("ERROR")
    
        print('Creando nueva sesión de Spark...\n')
    
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

        data = SPARK.read.csv(os.path.join(RUTA_OG, 'breast_cancer.csv'), header=True, inferSchema=True)

        # Contar el número de carpetas en el directorio de destino
        n_directories = len([d for d in os.listdir(RUTA_DEST) if os.path.isdir(os.path.join(RUTA_DEST, d))])

        ruta_destino = os.path.join(RUTA_DEST, f'breast_cancer_{n_directories}')

        data.write.parquet(ruta_destino)

        print(f'Datos guardados en {ruta_destino}')

        return ruta_destino, f'breast_cancer_{n_directories}'
    
    @staticmethod
    def transform_data(RUTA_OG, RUTA_DEST, SPARK):
        print('Pasando a la capa Business...')

        n_directories = len([d for d in os.listdir(RUTA_DEST) if os.path.isdir(os.path.join(RUTA_DEST, d))])
        data = SPARK.read.parquet(os.path.join(RUTA_OG, f'breast_cancer_{n_directories}'))

        ruta_destino = os.path.join(RUTA_DEST, f'breast_cancer_{n_directories}')

        #transformaciones

        data = data.withColumn('diagnosis' , when(data['diagnosis'] == 'M', 'Maligno').when(data['diagnosis'] == 'B', 'Benigno').otherwise(data['diagnosis']))

        old_cols = ["diagnosis","radius_mean","texture_mean","perimeter_mean","area_mean","smoothness_mean","compactness_mean","concavity_mean","concave points_mean","symmetry_mean","fractal_dimension_mean","radius_se","texture_se","perimeter_se","area_se","smoothness_se","compactness_se","concavity_se","concave points_se","symmetry_se","fractal_dimension_se","radius_worst","texture_worst","perimeter_worst","area_worst","smoothness_worst","compactness_worst","concavity_worst","concave points_worst","symmetry_worst","fractal_dimension_worst"]
        new_cols = ["Diagnóstico","Radio medio","Textura media","Perímetro medio","Área media","Suavidad media","Compacidad media","Concavidad media","Puntos cóncavos medios","Simetría media","Dimensión fractal media","Error estándar del radio","Error estándar de la textura","Error estándar del perímetro","Error estándar del área","Error estándar de la suavidad","Error estándar de la compacidad","Error estándar de la concavidad","Error estándar de los puntos cóncavos","Error estándar de la simetría","Error estándar de la dimensión fractal","Peor radio","Peor textura","Peor perímetro","Peor área","Peor suavidad","Peor compacidad","Peor concavidad","Peor puntuación de los puntos cóncavos","Peor simetría","Peor dimensión fractal"]
        data = data.select([col(old_col).alias(new_col) for old_col, new_col in zip(old_cols, new_cols)])

        data.write.parquet(ruta_destino)

        print(f'Datos transformados y guardados en {ruta_destino}')

        return ruta_destino, f'breast_cancer_{n_directories}'

    @staticmethod
    def get_kaggle():
        print('Pasando a la capa Raw...')
        dataset_name = 'uciml/breast-cancer-wisconsin-data'
        download_path = './raw'

        kaggle.api.dataset_download_files(dataset_name, download_path, unzip=True)
        og_name =  '.data/raw/'+os.listdir('.data/raw')[0]
        os.rename(og_name, '.data/raw/breast_cancer.csv')