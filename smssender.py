import requests
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import SMS, Customer, Campaign  # Assuming models are in models.py

class SmsSender:
    def __init__(self, api_secret, device_guid, base_url, db_session):
        self.api_secret = api_secret
        self.device_guid = device_guid
        self.base_url = base_url
        self.session = db_session

    def send_sms(self, sms_record, dummy=False):
        # If dummy is True, simulate sending and just print details
        if dummy:
            print(f"Dummy Mode: SMS to {sms_record.customer.Phone}: {sms_record.text}")
            sms_record.status = "sent"  # Mark as sent without sending
            sms_record.senddate = datetime.now() 
        else:
            # Prepare the actual message payload
            message = {
                "secret": self.api_secret,
                "mode": "devices",
                "device": self.device_guid,  # Using device GUID from constructor
                "sim": 1,
                "priority": 1,
                "phone": sms_record.customer.Phone,
                "message": sms_record.text
            }

            try:
                # Send the actual SMS
                response = requests.post(
                    url=f"{self.base_url}/api/send/sms", 
                    params=message, 
                    verify=False
                )
                result = response.json()

                # Handle the response and update the status
                if result.get("message") == "Message has been queued for sending!":
                    sms_record.status = "sent"
                    sms_record.senddate = datetime.now() 
                    print(f"SMS sent to {sms_record.customer.Name} successfully!")
                else:
                    sms_record.status = "failed"
                    print(f"Failed to send SMS to {sms_record.customer.Name}. Reason: {result.get('message')}")

            except Exception as e:
                sms_record.status = "failed"
                print(f"Exception occurred while sending SMS: {e}")
        
        # Commit the status update to the database
        self.session.commit()

    def send_campaign_sms(self, campaign_id, dummy=False):
        """
        Send SMS for a given campaign. 
        If dummy is True, it simulates sending and prints the message and phone without sending the actual SMS.
        """
        # Query for the SMS records that belong to the campaign and are pending
        pending_sms_records = self.session.query(SMS).filter_by(idcampaign=campaign_id, status="ready").all()

        if not pending_sms_records:
            print("No pending SMS records found for the campaign.")
            return

        # Send SMS for each pending record
        for sms_record in pending_sms_records:
            self.send_sms(sms_record, dummy=dummy)



