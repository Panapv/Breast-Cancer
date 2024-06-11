import boto3
from dotenv import load_dotenv
import os
 
load_dotenv()
   
class S3Client:
   
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION_NAME')
        )

    def create_s3_folder(self, bucket_name, folder_name):
        folder_key = f'{folder_name}/'  
        self.s3_client.put_object(Bucket=bucket_name, Key=folder_key)
        print(f"Carpeta {folder_name} creada en el bucket {bucket_name}\n")

    def upload_files(self, bucket_name, folder_path, folder_name):
        folder_key = f'{folder_name}/'  
        if os.path.isdir(folder_path):
            archivos = os.listdir(folder_path)
            for archivo in archivos:
                self.s3_client.upload_file(os.path.join(folder_path, archivo), bucket_name, os.path.join(folder_key, archivo))
                print(f"Uploaded {folder_path + '/' + archivo} to s3://{bucket_name}/{folder_key + archivo}")
        else:
            print("La ruta especificada no es una carpeta.")

        print()