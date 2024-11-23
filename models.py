from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaign'  # Name of the table in the database

    idcampaign = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(45), nullable=False)
    ForGender = Column(String(45), nullable=False)
    Text = Column(String(255), nullable=False)
    DaysBetweenSms = Column(Integer, nullable=False, default=0)
    Status = Column(String(45), nullable=False, default='init')

    def __repr__(self):
        return (f"<Campaign(idcampaign={self.idcampaign}, "
                f"Name='{self.Name}', ForGender='{self.ForGender}', "
                f"Text='{self.Text}', DaysBetweenSms={self.DaysBetweenSms}, Status={self.Status})>")
    
    def AddCustAll(self, session):
        # If the campaign targets "All", don't filter by Gender, otherwise apply the filter.
        print("Start AddCust All")
        if self.ForGender == 'All':
            customers = session.query(Customer).all()
        else:
            customers = session.query(Customer).filter_by(Gender=self.ForGender).all()

        # Calculate the cutoff date based on DaysBetweenSms
        if self.DaysBetweenSms > 0:
            cutoff_date = datetime.now() - timedelta(days=self.DaysBetweenSms)
        else:
            cutoff_date = None



        # For each customer, add an SMS record to the session if they are eligible
        for customer in customers:
            # Check if customer received an SMS in the last 'DaysBetweenSms' days
            # Skip customers with the name "skip"
            if customer.Name.lower() == "skip":
                print(f"Skipping customer {customer.Name} (id: {customer.idCustomers})")
                continue
            
            if cutoff_date:
                # Query to find the latest SMS sent to the customer
                last_sms = session.query(SMS).filter_by(idcustomer=customer.idCustomers).order_by(SMS.senddate.desc()).first()

                # If the customer has received an SMS after the cutoff date, skip adding a new SMS
                if last_sms and last_sms.senddate and last_sms.senddate > cutoff_date:
                    continue  # Skip this customer if they recently received an SMS

            # Use the smsText method to generate the text
            sms_text = self.smsText(customer)
            sms = SMS(
                idcampaign=self.idcampaign,
                idcustomer=customer.idCustomers,
                senddate=None,  # You can set a specific send date if needed
                status='Ready',  # Default status of the SMS
                text=sms_text,
                createdate=datetime.now()
            )
            session.add(sms)
        self.Status = 'ready'
        # Save all new SMS records
        session.commit()

    def smsText(self, customer):
        """
        Generate personalized SMS text for a given customer.
        :param customer: Customer object
        :return: Personalized SMS text
        """
        print("Start sms text")
        return self.Text.replace("{Name}", customer.Wolacz)


class Customer(Base):
    __tablename__ = 'customers'  # Name of the table in the database

    idCustomers = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(45), nullable=False)
    Gender = Column(String(45), nullable=False)
    Title = Column(String(45), nullable=False)
    Wolacz = Column(String(45), nullable=False)
    Phone = Column(String(45), nullable=False)

    def __repr__(self):
        return (f"<Customer(idCustomers={self.idCustomers}, "
                f"Name='{self.Name}', Gender='{self.Gender}', "
                f"Title='{self.Title}', Wolacz='{self.Wolacz}', Phone='{self.Phone})>")

class SMS(Base):
    __tablename__ = 'sms'  # Name of the table in the database

    idSMS = Column(Integer, primary_key=True, autoincrement=True)
    idcampaign = Column(Integer, ForeignKey('campaign.idcampaign', ondelete='SET NULL'), nullable=True)
    idcustomer = Column(Integer, ForeignKey('customers.idCustomers', ondelete='SET NULL'), nullable=True)
    senddate = Column(DateTime, nullable=True)
    status = Column(String(45), nullable=True)
    text = Column(String(45), nullable=True)
    createdate = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP')

    # Relationships
    campaign = relationship("Campaign", backref="sms_records")
    customer = relationship("Customer", backref="sms_records")

    def __repr__(self):
        return (f"<SMS(idSMS={self.idSMS}, idcampaign={self.idcampaign}, "
                f"idcustomer={self.idcustomer}, senddate={self.senddate}, "
                f"status='{self.status}', text='{self.text}', createdate={self.createdate})>")
