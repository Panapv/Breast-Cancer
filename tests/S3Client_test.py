import os, sys, tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from S3Client import S3Client
import boto3
from moto import mock_aws

@pytest.fixture
def s3_client():
    return S3Client()

@mock_aws
def test_upload_files(s3_client, mocker):
    bucket_name = 'test-bucket'
    folder_name = 'test-folder'

    # Creamos el bucket de prueba
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)

    # Creamos un directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        # Creamos archivos temporales con contenido simulado dentro del directorio temporal
        file1_path = os.path.join(temp_dir, 'file1.txt')
        file2_path = os.path.join(temp_dir, 'file2.txt')
        
        with open(file1_path, 'wb') as file1, open(file2_path, 'wb') as file2:
            file1.write(b'File 1 content')
            file2.write(b'File 2 content')

        # Simulamos os.listdir para devolver los nombres de los archivos temporales
        mocker.patch('os.listdir', return_value=[os.path.basename(file1_path), os.path.basename(file2_path)])

        # Ejecutamos el método que queremos probar
        s3_client.upload_files(bucket_name, temp_dir, folder_name)

        # Verificamos que los archivos se hayan subido correctamente
        objects = s3.list_objects(Bucket=bucket_name)
        assert len(objects['Contents']) == 2
        assert objects['Contents'][0]['Key'] == f'{folder_name}/file1.txt'
        assert objects['Contents'][1]['Key'] == f'{folder_name}/file2.txt'

@mock_aws
def test_create_s3_bucket(s3_client):
    bucket_name = 'test-bucket'

    # Ejecutamos el método que queremos probar
    s3_client.create_s3_bucket(bucket_name)

    # Verificamos que el bucket se haya creado correctamente
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
    assert bucket_name in [bucket['Name'] for bucket in buckets]

