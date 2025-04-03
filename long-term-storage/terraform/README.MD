# Long Term Storage

## Every hour data is queried to find data over 24 hours old (GMT Time). This is removed from the database and stored in an S3 bucket.
This folder is reponsible for making that happen.

**BUCKET NAME: c16-louis-data**

- terraform/ - Contains code for storage infrastructure
    - Creates S3 bucket
    - Creates lambda function from ECR image
    - Provides environmental variables in `terraform.tfvars`:
```
DB_USERNAME=<database_username>
DB_PASSWORD=<database_password>
DB_HOST=<database_url>
DB_PORT=1433
DB_NAME="lmnh_plants" 
PRODUCTION_MODE=true #This is for testing, when set to false or not included data is **NOT** removed from the database
BUCKET_NAME="c16-louis-data"
```

- S3 Bucket - Contains historical / aggregated data. Structure:
    - historical/ - raw historical data
        -  [Year]-[Month]/[day]/measurement_[hour].parquet | Files are stored hourly.
    - aggregate/ - aggregated historical data (optional)
    - metadata/ other archived data (optional)

- lambda/
    - Dockerfile for creating the image
    - Requirements for the docker image / to run it generally
    - `move_storage.py` contains code for the lambda service
        - Gets data from the database
        - Creates a dataframe and stores a parquet file in memory
        - Adds it to the bucket with the structure above
        - Removes rows from the databases
        - Environmental variables required are above
        - Also needs `BasicLambdaExecutionRole` to be able to upload to S3