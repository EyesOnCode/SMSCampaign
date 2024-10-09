from flask import Flask, render_template, request, redirect, flash
from smssender import SmsSender # Import the SMS sending class
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Campaign

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

if __name__ == '__main__':
    app.run(debug=True)
