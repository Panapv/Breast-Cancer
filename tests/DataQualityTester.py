from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
import pyspark.sql.functions as F
import json

class DataQualityTester:
    
    def __init__(self, data_path, schema_path="tests/schemas/schema.json"):
        self.spark = SparkSession.builder \
        .appName("dataquality-pyspark-testing") \
        .master("local[*]") \
        .getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR") 
        self.data = self.load_data(data_path)
        self.schema_path = schema_path
        
    def test_data(self, print_results=True):
        if print_results:
            print('El esquema de datos es VÁLIDO') if self.schema_is_valid() else print('El esquema de datos es INVÁLIDO')
            print('El conjunto de datos NO contine valores NULOS') if self.is_nulls_free() else print('El conjunto de datos CONTIENE valores NULOS')
            print('El conjunto de datos NO contine valores DUPLICADOS') if self.is_duplicates_free() else print('El conjunto de datos CONTIENE valores DUPLICADOS')
            print('Los datos son VÁLIDOS') if self.format_is_valid() else print('El formato de los datos es INVÁLIDO')
    
        return (self.schema_is_valid() and
            self.is_nulls_free() and
            self.is_duplicates_free() and
            self.format_is_valid())
    
    def load_data(self, data_path):
        data = self.spark.read.option("basePath", data_path).parquet(data_path)
        return data
    
    # Comprueba que el esquema del DataFrame sea el esperado.
    def schema_is_valid(self):
        with open(self.schema_path, "r") as f:
            saved_schema_json = f.read()
            
        saved_schema = StructType.fromJson(json.loads(saved_schema_json))
        current_schema = self.data.schema
        return True if saved_schema == current_schema else False
    
    # Revisa que no haya valores nulos
    def is_nulls_free(self):
        null_counts = self.data.agg(*[F.sum(F.col(c).isNull().cast("int")).alias(c) for c in self.data.columns]).collect()[0]
        return False if any(null_counts) else True
    
    # Revisa que no existan filas duplicadas
    def is_duplicates_free(self):
        total_count = self.data.count()
        distinct_count = self.data.dropDuplicates().count()
        return True if total_count == distinct_count else False
    
    # Revisa que todas las columnas contengan los datos esperados
    def format_is_valid(self):
        # Comprueba la columna 'Diagnóstico'
        diagnostico_values = self.data.select("diagnóstico").distinct().collect()
        values = {row.diagnóstico for row in diagnostico_values}
        diagnostico_is_correct = (sorted(list(values)) == sorted(list({"Benigno", "Maligno"})))
        if not diagnostico_is_correct: 
            return False
        # Comprueba el resto de columnas de métricas
        data_metrics_only = self.data.select(*self.data.columns[1:])
        for column in data_metrics_only.columns:
            # Verificar si todas las celdas de la columna son de tipo Double
            if not all(isinstance(row[column], float) or isinstance(row[column], int)
                    for row in data_metrics_only.select(column).collect()):
                return False
        return True