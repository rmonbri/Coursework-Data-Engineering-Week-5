# Overview
The script `detect-anomalies.py` detects anomalies in the last 15 minute's worth of measurements from the plant sensors in the LMNH museum.
An anomaly is defined as a temperature or moisture content measurement outlier with a value beyond 2.5 standard deviations from the mean of its measurement type, for a specific plant. We determine anomalies in this way using Z-Score.

The script `send_email.py` sends an email directly to the botanist responsible for the plant with the anomaly. 
Emails include information on plant name, type, id, and sensor issue.

# Pre-requisites
- Run `pip3 install -r requirements.txt` to install any dependencies when testing this file.
- Put the short-term measurements database details in an env of the following format
```
DB_HOST=c16-louis-db.c57vkec7dkkx.eu-west-2.rds.amazonaws.com
DB_PORT=1433
DB_USERNAME=louis_admin
DB_PASSWORD=MvYmg8huy458
DB_NAME=lmnh_plants
```

# Usage

- `python3 detect_anomalies.py` will run the script, outputting a dictionary of form `{'moisture':[plant_ids] ,'temperature':[plant_ids]}` which contains the plant ids that had outliers and can be used as an input for the send_email script.
- `send_email.py` takes input of the form `{'moisture':[plant_ids] ,'temperature':[plant_ids]}`, which contains the plant ids that had outliers for moisture and temperature and sends an email to the botanists assigned to the specific plants using AWS SES.