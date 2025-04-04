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

## Updated Pipeline:

- To take advantage of being able to run multiple lambdas, `pipeline.py` was adjusted to take an `event` consisting of a dict containing a `plant_id`.
- `short-term-worker/worker.py` Will spin up an initial instance and from there create 50 workers, one for each plant.
- Each individual worker will perform a HTTP request and update the database for the plant_id it was assigned.
- This was added to fix long loading times encountered, but was not as neat as I would've liked.
- Both images and lambdas are defined in `terraform/`
- `worker.py` can be run independantly, but it is dependant on an ARN for a function.

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