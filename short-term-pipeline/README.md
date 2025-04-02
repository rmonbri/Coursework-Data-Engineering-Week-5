# Short term DB pipeline

This pipeline extracts, transforms and loads relevant data into the measurement table in the
lmnh_plants database

---

## Pipeline Overview

The pipeline is split into 3 main components:

1. extract.py: Connects to the API and extracts all the plant measurement data using multiprocessing, saving the data in 
a csv.

2. transform.py: Reads the plant measurement csv and transforms the data into the required format for the database, saving
the results in a new clean csv.

3. load.py: Loads the cleaned data into the lmnh_plants short term database.

4. pipeline.py: Connects the extract, transform and load script to have a single seamless pipeline.

To run the pipeline:

`python pipeline.py`


---

### Requirements

- A .env file has to be stored in the directory with the following variables:

```
DB_HOST=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_PORT=
```


- To install the required dependencies run:

`pip install -r requirements.txt`