import boto3
from dotenv import load_dotenv
import os
import botocore
 
load_dotenv()
   
class S3Client:
   
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION_NAME')
        )

    def upload_files(self, bucket_name, folder_path, folder_name):
        folder_key = f'{folder_name}/' 
        print(f"Carpeta {folder_name} creada en el bucket {bucket_name}\n")
        
        if os.path.isdir(folder_path):
            archivos = os.listdir(folder_path)
            for archivo in archivos:
                self.s3_client.upload_file(os.path.join(folder_path, archivo), bucket_name, os.path.join(folder_key, archivo))
                print(f"Uploaded {folder_path + '/' + archivo} to s3://{bucket_name}/{folder_key + archivo}")
        else:
            print("La ruta especificada no es una carpeta.")

        print()
    
    def create_s3_bucket(self, bucket_name):
        try:
            region = os.environ.get('AWS_REGION_NAME')
        
            if region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        
            print(f"Bucket '{bucket_name}' creado en la región: {region}\n")
        except botocore.exceptions.ClientError as e:
            print(f"Error occurred: {e}")