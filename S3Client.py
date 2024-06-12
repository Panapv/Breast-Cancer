import boto3
from dotenv import load_dotenv
import os
import botocore

"""Cargamos todas las variables de entorno."""
load_dotenv()
   
class S3Client:
   
    def __init__(self):
        """Inicializamos la clase y creamos un cliente de AWS con las credenciales correspondientes."""

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION_NAME')
        )

    def upload_files(self, bucket_name, folder_path, folder_name):
        """Este método sube los ficheros al bucket y carpeta indicados por parámetros.""" 

        folder_key = f'{folder_name}/' 
        print(f"Carpeta {folder_name} creada en el bucket {bucket_name}\n")
        
        # Comprueba si la ruta especificada existe.
        if os.path.isdir(folder_path):
            archivos = os.listdir(folder_path)

            # Recorre los archivos que se encuentran en la ruta y los sube uno a uno.
            for archivo in archivos:
                self.s3_client.upload_file(os.path.join(folder_path, archivo), bucket_name, os.path.join(folder_key, archivo))
                print(f"Uploaded {folder_path + '/' + archivo} to s3://{bucket_name}/{folder_key + archivo}")
        else:
            print("La ruta especificada no es una carpeta.")
        print()
    
    def create_s3_bucket(self, bucket_name):
        """Este método crea un nuevo bucket en AWS."""

        try:
            region = os.environ.get('AWS_REGION_NAME')
        
            # Crea el bucket
            self.s3_client.create_bucket(Bucket=bucket_name)
        
            print(f"Bucket '{bucket_name}' creado en la región: {region}\n")
        except botocore.exceptions.ClientError as e:
            print(f"Error occurred: {e}")