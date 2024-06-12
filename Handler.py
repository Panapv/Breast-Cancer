from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import when
import os
import kaggle

class HandlerBranchCode:

    @staticmethod
    def newSession(name):
        """Este método crea una nueva sesión de Spark.
        
        Args:
            name (str): Nombre de la sesión de Spark

        Returns:
            spark: Nueva sesión de Spark
        """
        spark = SparkSession.builder \
            .appName(name) \
            .getOrCreate()
        
        # Ponemos el LogLevel en ERROR para que muestre los ERRORES fatales de Spark por terminal.
        spark.sparkContext.setLogLevel("ERROR")
    
        print('Creando nueva sesión de Spark...\n')
        return spark

    @staticmethod
    def partition_folder(RUTA):
        """Este método crea carpetas en caso de que no existan.
        
        Args:
            RUTA (str): Ruta en la quieres crear la carpeta.

        Returns:
            path: Ruta de la carpeta
        """
        path = os.path.join(str(RUTA))
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def clean_data(RUTA_OG, RUTA_DEST, SPARK):
        """Este método limpia y guarda los datos en la capa de staging.
        
        Args:
            RUTA_OG (str): Ruta origen de los datos.\n 
            RUTA_DEST (str): Ruta destino de los datos.\n 
            SPARK (obj): Spark session  

        Returns:
            ruta_destino: Ruta del destino de los datos.\n 
            f'breast_cancer_{n_directories}': Nueva versión de los datos tras la ejecución.
        """

        print('Pasando a la capa Staging...')
        
        data = SPARK.read.csv(os.path.join(RUTA_OG, 'breast_cancer.csv'), header=True, inferSchema=True)

        # Contar el número de carpetas en el directorio de destino.
        n_directories = len([d for d in os.listdir(RUTA_DEST) if os.path.isdir(os.path.join(RUTA_DEST, d))])

        ruta_destino = os.path.join(RUTA_DEST, f'breast_cancer_{n_directories}')

        # Guardamos los datos en formato .parquet.
        data.write.parquet(ruta_destino)

        print(f'Datos guardados en {ruta_destino}')
        return ruta_destino, f'breast_cancer_{n_directories}'
    
    @staticmethod
    def transform_data(RUTA_OG, RUTA_DEST, SPARK):
        """Este método transfoma los datos para adaptarse a nuestro modelo de negocio y los guarda en la capa de business.
        
        Args:
            RUTA_OG (str): Ruta origen de los datos.\n 
            RUTA_DEST (str): Ruta destino de los datos.\n 
            SPARK (obj): Spark session.

        Returns:
            ruta_destino: Ruta del destino de los datos.\n 
            f'breast_cancer_{n_directories}': Nueva versión de los datos tras la ejecución.
        """

        print('Pasando a la capa Business...')

        n_directories = len([d for d in os.listdir(RUTA_DEST) if os.path.isdir(os.path.join(RUTA_DEST, d))])
        data = SPARK.read.parquet(os.path.join(RUTA_OG, f'breast_cancer_{n_directories}'))

        ruta_destino = os.path.join(RUTA_DEST, f'breast_cancer_{n_directories}') 

        # Cambiamos la columna de diagnosis de (M/B) a (Maligno/Benigno), para facilitar la compresión de los datos a la hora de hacer búsquedas.
        data = data.withColumn('diagnosis' , when(data['diagnosis'] == 'M', 'Maligno').when(data['diagnosis'] == 'B', 'Benigno').otherwise(data['diagnosis']))

        # Traducimos el nombre de las columnas al español. 
        old_cols = ["diagnosis","radius_mean","texture_mean","perimeter_mean","area_mean","smoothness_mean","compactness_mean","concavity_mean","concave points_mean","symmetry_mean","fractal_dimension_mean","radius_se","texture_se","perimeter_se","area_se","smoothness_se","compactness_se","concavity_se","concave points_se","symmetry_se","fractal_dimension_se","radius_worst","texture_worst","perimeter_worst","area_worst","smoothness_worst","compactness_worst","concavity_worst","concave points_worst","symmetry_worst","fractal_dimension_worst"]
        new_cols = ["Diagnóstico","Radio medio","Textura media","Perímetro medio","Área media","Suavidad media","Compacidad media","Concavidad media","Puntos cóncavos medios","Simetría media","Dimensión fractal media","Error estándar del radio","Error estándar de la textura","Error estándar del perímetro","Error estándar del área","Error estándar de la suavidad","Error estándar de la compacidad","Error estándar de la concavidad","Error estándar de los puntos cóncavos","Error estándar de la simetría","Error estándar de la dimensión fractal","Peor radio","Peor textura","Peor perímetro","Peor área","Peor suavidad","Peor compacidad","Peor concavidad","Peor puntuación de los puntos cóncavos","Peor simetría","Peor dimensión fractal"]
        data = data.select([col(old_col).alias(new_col) for old_col, new_col in zip(old_cols, new_cols)])

        # Guardamos los datos en formato '.parquet'.
        data.write.parquet(ruta_destino)

        print(f'Datos transformados y guardados en {ruta_destino}')
        return ruta_destino, f'breast_cancer_{n_directories}'

    @staticmethod
    def get_kaggle():
        """Este método accede a la API de Kaggle y carga los datos en la capa raw."""

        print('Pasando a la capa Raw...')
        dataset_name = 'uciml/breast-cancer-wisconsin-data'
        download_path = './data/raw'

        # En caso de que venga comprimido este método lo descomprime automaticamente con el atributo 'unzip=True'.
        kaggle.api.dataset_download_files(dataset_name, download_path, unzip=True)
        og_name =  './data/raw/'+os.listdir('./data/raw')[0]

        # Cambiamos el nombre del archivo a 'breast_cancer.csv'.
        os.rename(og_name, './data/raw/breast_cancer.csv')