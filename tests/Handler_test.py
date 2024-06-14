import sys
import os
import pytest
from pyspark.sql import SparkSession
import tempfile
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Handler import HandlerBranchCode

# Configuración de la sesión de Spark
@pytest.fixture(scope="session")
def spark_session():
    spark = SparkSession.builder \
        .appName("pytest-pyspark-testing") \
        .master("local[*]") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_partition_folder(tmpdir):
    # Define la ruta para el testing
    test_path = tmpdir.join("test_folder")
    with patch("os.makedirs") as mock_makedirs:
        returned_path = HandlerBranchCode.partition_folder(test_path)

        # Comprueba que os.makedirs se haya llamado con los argumentos correctos
        mock_makedirs.assert_called_once_with(str(test_path), exist_ok=True)

        # Comprueba que el resultado sea la ruta esperada
        assert returned_path == str(test_path)
        
def test_clean_data(spark_session):
    # Se crean directorios temporales para rutas de prueba
    with tempfile.TemporaryDirectory() as ruta_og, tempfile.TemporaryDirectory() as ruta_dest:
        
        # Se crea un archivo CSV temporal en la ruta origen
        csv_path = os.path.join(ruta_og, 'breast_cancer.csv')
        with open(csv_path, 'w') as f:
            f.write("id,value\n1,foo\n2,bar\n")
        
        # Se ejecuta el método clean_data
        ruta_destino, version = HandlerBranchCode.clean_data(ruta_og, ruta_dest, spark_session)
        
        # Verifica que el archivo parquet se haya escrito en la ruta destino
        assert os.path.exists(ruta_destino)
        assert os.path.isdir(ruta_destino)
        
        # Verificar que la versión sea correcta y por lo tanto el conteo de directorios también lo es
        assert version == f'breast_cancer_0'
        
        # Verifica que los datos se hayan escrito correctamente en formato parquet
        df = spark_session.read.parquet(ruta_destino)
        assert df.count() == 2
        assert df.filter(df.value == "foo").count() == 1
        assert df.filter(df.value == "bar").count() == 1
       
def test_transform_data(spark_session):
    # Crea directorios temporales para rutas de prueba
    with tempfile.TemporaryDirectory() as ruta_og, tempfile.TemporaryDirectory() as ruta_dest:
        # Crea un DataFrame de prueba y lo escribe como parquet
        data = [("M", 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0),
                ("B", 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1, 12.1, 13.1, 14.1, 15.1, 16.1, 17.1, 18.1, 19.1, 20.1, 21.1, 22.1, 23.1, 24.1, 25.1, 26.1, 27.1, 28.1, 29.1, 30.1)]
        columns = ["diagnosis","radius_mean","texture_mean","perimeter_mean","area_mean","smoothness_mean","compactness_mean","concavity_mean","concave points_mean","symmetry_mean","fractal_dimension_mean","radius_se","texture_se","perimeter_se","area_se","smoothness_se","compactness_se","concavity_se","concave points_se","symmetry_se","fractal_dimension_se","radius_worst","texture_worst","perimeter_worst","area_worst","smoothness_worst","compactness_worst","concavity_worst","concave points_worst","symmetry_worst","fractal_dimension_worst"]
        
        df = spark_session.createDataFrame(data, columns)
        df.write.parquet(os.path.join(ruta_og, 'breast_cancer_0'))

        # Ejecuta el método transform_data
        ruta_destino, version = HandlerBranchCode.transform_data(ruta_og, ruta_dest, spark_session)
        
        # Verifica que el archivo parquet se haya escrito en la ruta destino
        assert os.path.exists(ruta_destino)
        assert os.path.isdir(ruta_destino)
        
        # Verificar que la versión sea correcta y por lo tanto el conteo de directorios también lo es
        assert version == f'breast_cancer_0'
        
        # Verifica que los datos se hayan transformado correctamente
        df_transformed = spark_session.read.parquet(ruta_destino)
        assert df_transformed.filter(df_transformed.Diagnóstico == "Maligno").count() == 1
        assert df_transformed.filter(df_transformed.Diagnóstico == "Benigno").count() == 1
        assert "Diagnóstico" in df_transformed.columns
        assert "Radio medio" in df_transformed.columns
        assert "Textura media" in df_transformed.columns

def test_get_kaggle():
    # Ruta de descarga simulada y dataset simulado
    download_path = './data/raw'
    dataset_name = 'uciml/breast-cancer-wisconsin-data'
    
    with patch('kaggle.api.dataset_download_files') as mock_download_files:
        # Simulamos la descarga
        mock_download_files.return_value = None
        
        # Ejecutamos el método get_kaggle
        HandlerBranchCode.get_kaggle()
        
        # Verificamos que la función de descarga se llamó con los argumentos correctos
        mock_download_files.assert_called_once_with(dataset_name, download_path, unzip=True)

        # Verificamos que se haya renombrado un archivo en la carpeta raw
        assert any(file.startswith('breast_cancer') for file in os.listdir(download_path))