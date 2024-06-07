from Handler import HandlerBranchCode

def main():
    spark = HandlerBranchCode.newSession('ETL - Breast Cancer')

    path_staging = HandlerBranchCode.partition_folder('.\\staging')
    HandlerBranchCode.clean_data('.\\raw\\breast_cancer.csv', path_staging, spark)

    path_business = HandlerBranchCode.partition_folder('.\\business')
    HandlerBranchCode.transform_data('.\\staging\\breast_cancer', path_business, spark)

    spark.stop()

if __name__ == "__main__":
    main()