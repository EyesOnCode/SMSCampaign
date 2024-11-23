from flask import Flask, render_template, request, redirect, flash, url_for
from smssender import SmsSender # Import the SMS sending class
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Campaign, SMS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for flashing messages

# Load configuration from a config.json file
def load_config(filename='config.json'):
    with open(filename, 'r') as config_file:
        config = json.load(config_file)
    return config

config = load_config()

# Initialize the SMS sender with values from the config
api_secret = config['api_secret']
device_guid = config['device_guid']
base_url = config['base_url']

# Database setup
DATABASE_URI = (f"mysql+pymysql://{config['db_user']}:{config['db_password']}"
f"@{config['db_host']}/{config['db_name']}")
# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Homepage with SMS sending form
@app.route('/', methods=['GET'])
def index():
    # Query to get all campaigns from the database
    all_campaigns = session.query(Campaign).all()
    # Prepare a dictionary to store SMS counts for campaigns in "Ready" status
    sms_counts = {}
    for campaign in all_campaigns:
        if campaign.Status == 'ready':
            sms_count = session.query(SMS).filter_by(idcampaign=campaign.idcampaign).count()
            sms_counts[campaign.idcampaign] = sms_count
        else:
            sms_counts[campaign.idcampaign] = None  # No count for campaigns not in "Ready" status

    # Render a template to display the campaigns
    return render_template('index.html', campaigns=all_campaigns, sms_counts=sms_counts)

@app.route('/addCampaign', methods=['GET'])
def add_campaign_page():
    # Renders the form page to add a new campaign
    return render_template('addCampaign.html')

@app.route('/addCampaign', methods=['POST'])
def add_campaign():
    # Get form data
    name = request.form['name']
    for_gender = request.form['for_gender']
    text = request.form['text']
    days_between_sms = int(request.form['days_between_sms'])

    # Create a new Campaign object and add it to the database
    new_campaign = Campaign(
        Name=name,
        ForGender=for_gender,
        Text=text,
        DaysBetweenSms=days_between_sms
    )
    session.add(new_campaign)
    session.commit()

    # Redirect back to the campaign list after adding the new campaign
    return redirect(url_for('index'))

@app.route('/editCampaign/<int:id>', methods=['GET', 'POST'])
def edit_campaign(id):
    # Retrieve the campaign by ID
    campaign = session.query(Campaign).get(id)

    # Check if the campaign exists
    if not campaign:
        return "Campaign not found", 404

    if request.method == 'POST':
        # Get form data and update the campaign
        campaign.Name = request.form['name']
        campaign.ForGender = request.form['for_gender']
        campaign.Text = request.form['text']
        campaign.DaysBetweenSms = int(request.form['days_between_sms'])
        
        # Commit the updated campaign to the database
        session.commit()

        # Redirect back to the campaign list after updating
        return redirect(url_for('index'))

    # Render the form with existing campaign data for editing
    return render_template('addCampaign.html', campaign=campaign, edit=True)


@app.route('/delete_campaign/<int:campaign_id>', methods=['POST'])
def delete_campaign(campaign_id):
    # Find the campaign by its ID
    campaign = session.query(Campaign).filter_by(idcampaign=campaign_id).first()

    if not campaign:
        flash('Campaign not found!', 'error')
        return redirect(url_for('index'))

    # Delete associated SMS records
    session.query(SMS).filter_by(idcampaign=campaign_id).delete()

    # Delete the campaign itself
    session.delete(campaign)
    session.commit()

    flash(f'Campaign {campaign.Name} and its associated SMS records were deleted successfully.', 'success')

    # Redirect back to the campaign list
    return redirect(url_for('index'))
@app.route('/edit_campaign/<int:id>', methods=['GET', 'POST'])
def edit_campaign_page(id):
    campaign = session.query(Campaign).get(id)
    if request.method == 'POST':
        campaign.Name = request.form['name']
        campaign.ForGender = request.form['for_gender']
        campaign.Text = request.form['text']
        campaign.DaysBetweenSms = request.form['days_between_sms']
        campaign.Status = request.form['status']
        session.commit()
        return redirect(url_for('index'))
    return render_template('addCampaign.html', campaign=campaign, edit=True)

@app.route('/campaign/<int:id>', methods=['GET'])
def campaign_details(id):
    # Query for the specific campaign and its related SMS records
    campaign = session.query(Campaign).filter_by(idcampaign=id).first()
    sms_records = session.query(SMS).filter_by(idcampaign=id).all()

    if not campaign:
        return "Campaign not found", 404

    # Render a template to display the campaign details and SMS records
    return render_template('campaign_details.html', campaign=campaign, sms_records=sms_records)


@app.route('/prepareCampaign/<int:id>', methods=['POST'])
def prepare_campaign(id):
    # Retrieve the campaign by ID
    campaign = session.query(Campaign).get(id)

    # Check if the campaign exists
    if not campaign:
        return "Campaign not found", 404

    # Generate SMS records using the AddCustAll method
    campaign.AddCustAll(session)

    # Redirect back to the campaign list
    return redirect(url_for('index'))

@app.route('/clear_campaign/<int:id>', methods=['POST'])
def clear_campaign(id):
    # Query the campaign
    campaign = session.query(Campaign).filter_by(idcampaign=id).first()

    if not campaign:
        return "Campaign not found", 404

    # Check if the campaign status is "Ready"
    if campaign.Status == 'ready':
        # Delete all SMS records associated with this campaign
        session.query(SMS).filter_by(idcampaign=id).delete()

        # Update the campaign status to "init"
        campaign.Status = 'init'
        session.commit()

    # Redirect back to the index page
    return redirect(url_for('index'))

@app.route('/send_sms/<int:id>', methods=['POST'])
def send_sms(id):
    # Query the campaign
    campaign = session.query(Campaign).filter_by(idcampaign=id).first()

    if not campaign:
        return "Campaign not found", 404

    # Check if the campaign status is "Ready"
    if campaign.Status == 'Ready':
        # Initialize the SMS sender
        sms_sender = SmsSender(
            config['api_secret'], 
            config['device_guid'], 
            config['base_url'], 
            session
        )

        # Send SMS for the campaign
        sms_sender.send_campaign_sms(id)

        # Optionally, update the campaign status to indicate SMSs have been sent
        campaign.Status = 'Completed'
        session.commit()

    # Redirect back to the index page
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
