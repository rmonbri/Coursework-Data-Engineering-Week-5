# Overview
The script `detect-anomalies.py` detects anomalies in the last n measurements from the plant sensors in the LMNH museum.
An anomaly is defined as a temperature or moisture content measurement outlier with a value beyond 2.5 standard deviations from the mean of its measurement type, for a specific plant. We determine anomalies in this way using Z-Score.

The script `send_email.py` sends an email directly to the botanist responsible for the plant with the anomaly. 
Emails include information on plant name, type, id, and sensor issue.

# Pre-requisites
Please run `pip3 install -r requirements.txt` to install any dependencies when testing this file.
