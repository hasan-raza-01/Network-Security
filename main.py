from package.pipeline.stage_01_data_ingestion import DataIngestionPipeline



STAGE_NAME = "Data Ingestion"

print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} initiated <<<<<<<<<<<<<<<<<<<<<")
obj = DataIngestionPipeline()
obj.main()
print(f"\n>>>>>>>>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<<<<<<<<<<")


