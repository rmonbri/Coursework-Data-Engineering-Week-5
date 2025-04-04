"""Script to send an email to botanists with plants under their
care that have faulty sensors based on anomaly detection script"""

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import pymssql
import boto3

from detect_anomalies import get_recent_measurements, detect_plant_risks, add_zscore_columns


def get_connection_to_db() -> pymssql.Connection:
    """Gets a pymssql connection to the short term MS SQL short-term DB"""
    load_dotenv()
    return pymssql.connect(host=os.getenv("DB_HOST"),
                           database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USERNAME"),
                           password=os.getenv("DB_PASSWORD"),
                           port=os.getenv("DB_PORT"))


def get_botanist_details_from_db(plant_ids: list[int]):
    """Connecting to database and retrieving botanist details"""
    conn = get_connection_to_db()

    curr = conn.cursor()

    plant_ids_list = ",".join(["%s"] * len(plant_ids))

    query = f"""SELECT plant_id, plant_name, botanist_name, botanist_email
                FROM plant p
                JOIN plant_type pt ON pt.plant_type_id = p.plant_type_id
                JOIN botanist b ON b.botanist_id = p.botanist_id
                WHERE plant_id IN ({plant_ids_list})"""

    curr.execute(query, tuple(plant_ids))
    results = curr.fetchall()
    conn.close()

    botanist_details = [{
        "plant_id": row[0],
        "plant_name": row[1],
        "botanist_name": row[2],
        "botanist_email": row[3]
    } for row in results]

    return botanist_details


def format_plant_issues_data(anomaly_data: list[dict], affected_plants: list[int]) -> dict:
    """Formatting all issues associated with the same plant_id into one sentence"""
    plant_issues = {}

    for plant_id in affected_plants:
        issues = []
        if plant_id in anomaly_data["moisture"]:
            issues.append("soil moisture sensor")
        if plant_id in anomaly_data["temperature"]:
            issues.append("plant temperature sensor")
        plant_issues[plant_id] = ", ".join(issues)
    return plant_issues


def group_affected_plants_by_botanist(botanist_details: list[dict], plant_issues: dict) -> dict:
    """Group affected plants under the botanist responsible for them."""
    botanist_plant_map = {}

    for botanist in botanist_details:
        email = botanist["botanist_email"]
        plant_id = botanist["plant_id"]
        plant_name = botanist["plant_name"]

        if plant_id in plant_issues:
            if email not in botanist_plant_map:
                botanist_plant_map[email] = {
                    "botanist_name": botanist["botanist_name"],
                    "issues": []
                }
            botanist_plant_map[email]["issues"].append(
                f"Plant {plant_name} (ID: {plant_id}) has issues: {plant_issues[plant_id]}"
            )

    return botanist_plant_map


def generate_email_body(botanist_name: str, issues: list[str]) -> str:
    """Generate a well-formatted email body for a botanist."""
    return f"""Dear {botanist_name},

The following plants need your attention:

{chr(10).join(issues)}

Regards,
Anomaly Detection Team"""


def format_botanist_notification(botanist_details: list[dict], plant_issues: dict) -> list:
    """Format notifications so each botanist gets ONE email listing all affected plants."""
    botanist_plant_map = group_affected_plants_by_botanist(
        botanist_details, plant_issues)

    email_notifications = []
    for email, details in botanist_plant_map.items():
        email_body = generate_email_body(
            details["botanist_name"], details["issues"])

        email_notifications.append({
            "email": email,
            "subject": "Plant Monitoring Alert",
            "body": email_body
        })

    return email_notifications


def send_email(notification: dict):
    """Send an email using AWS SES."""
    client = boto3.client("ses", region_name="eu-west-2")
    message = MIMEMultipart()
    message["Subject"] = notification["subject"]
    message["From"] = "trainee.hadia.fadlelmawla@sigmalabs.co.uk"
    message["To"] = "trainee.hadia.fadlelmawla@sigmalabs.co.uk"

    body = MIMEText(notification["body"], "plain")
    message.attach(body)

    client.send_raw_email(
        Source=message["From"],
        Destinations=[message["To"]],
        RawMessage={"Data": message.as_string()}
    )


def run_email_pipeline():
    """Runs the full anomaly detection and email notification pipeline."""
    print("Fetching recent measurements...")
    recent_measurements = get_recent_measurements()
    recent_measurements = add_zscore_columns(recent_measurements)

    print("Detecting anomalies...")
    anomalies = detect_plant_risks(recent_measurements)
    print(f"anomalies detected: {anomalies}")
    affected_plants = anomalies["moisture"] + anomalies["temperature"]
    if not affected_plants:
        print("No anomalies detected. No emails sent.")
        return
    plant_issues = format_plant_issues_data(anomalies, affected_plants)

    print("Fetching botanist details...")
    botanist_details = get_botanist_details_from_db(affected_plants)

    print("Formatting email notifications...")
    notifications = format_botanist_notification(
        botanist_details, plant_issues)

    print(f"Sending {len(notifications)} emails...")
    for notification in notifications:
        send_email(notification)

    print("Email pipeline completed successfully.")


def lambda_handler(event, context):
    """AWS Lambda entry point."""
    try:
        run_email_pipeline()
        return {"statusCode": 200, "body": "Email notifications sent successfully."}

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Email failed to send with error: {str(e)}"
        }


if __name__ == "__main__":
    run_email_pipeline()
