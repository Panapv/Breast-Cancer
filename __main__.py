from Handler import HandlerBranchCode
import os

def main():
    spark = HandlerBranchCode.newSession('ETL - Breast Cancer')

    path_staging = HandlerBranchCode.partition_folder(os.path.join('.', 'staging'))
    HandlerBranchCode.clean_data(os.path.join('.', 'raw'), path_staging, spark)

    path_business = HandlerBranchCode.partition_folder(os.path.join('.', 'business'))
    HandlerBranchCode.transform_data(os.path.join('.', 'staging'), path_business, spark)

    spark.stop()

if __name__ == "__main__":
    main()