from Handler import HandlerBranchCode
from S3Client import S3Client
import os

def main():
    s3 = S3Client()
    spark = HandlerBranchCode.newSession('ETL - Breast Cancer')

    bucket_name = 'breast-cancer-s3'
    s3.create_s3_bucket(bucket_name)

    HandlerBranchCode.get_kaggle() # Comprobar si tienes las credenciales en .kaggle
    s3.upload_files(bucket_name, './raw', 'raw')

    path_staging = HandlerBranchCode.partition_folder(os.path.join('.', 'staging'))
    staging_files_path = HandlerBranchCode.clean_data(os.path.join('.', 'raw'), path_staging, spark)
    s3.upload_files(bucket_name, staging_files_path[0], os.path.join('staging', staging_files_path[1]))

    path_business = HandlerBranchCode.partition_folder(os.path.join('.', 'business'))
    business_files_path = HandlerBranchCode.transform_data(os.path.join('.', 'staging'), path_business, spark)
    s3.upload_files(bucket_name, business_files_path[0], os.path.join('business', business_files_path[1]))

    spark.stop()

if __name__ == "__main__":
    main()