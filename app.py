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

    # Render a template to display the campaigns
    return render_template('index.html', campaigns=all_campaigns)

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


if __name__ == '__main__':
    app.run(debug=True)
