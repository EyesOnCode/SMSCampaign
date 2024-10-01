from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaign'  # Name of the table in the database

    idcampaign = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(45), nullable=False)
    ForGender = Column(String(45), nullable=False)
    Text = Column(String(45), nullable=False)

    def __repr__(self):
        return (f"<Campaign(idcampaign={self.idcampaign}, "
                f"Name='{self.Name}', ForGender='{self.ForGender}', "
                f"Text='{self.Text}')>")
    
    def AddCustAll(self, session):
        # If the campaign targets "All", don't filter by Gender, otherwise apply the filter.
        if self.ForGender == 'All':
            customers = session.query(Customer).all()
        else:
            customers = session.query(Customer).filter_by(Gender=self.ForGender).all()

        
        # Dla każdego klienta dodaj rekord SMS do sesji
        for customer in customers:
            sms_text = self.Text.replace("{Name}", customer.Wolacz)  # Personalizowanie treści SMS
            sms = SMS(
                idcampaign=self.idcampaign,
                idcustomer=customer.idCustomers,
                senddate=None,  # Możesz ustawić datę wysyłki, jeśli jest już znana
                status='Pending',  # Domyślny status wiadomości
                text=sms_text,
                createdate=datetime.now()
            )
            session.add(sms)
        
        # Zapisz wszystkie nowe rekordy SMS
        session.commit()

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
