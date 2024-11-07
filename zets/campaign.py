from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaign'  # Name of the table in the database

    idcampaign = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(45), nullable=False)
    ForGender = Column(String(45), nullable=False)
    Text = Column(String(45), nullable=False)
    DaysBetweenSms = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"<Campaign(idcampaign={self.idcampaign}, "
                f"Name='{self.Name}', ForGender='{self.ForGender}', "
                f"Text='{self.Text}')>,DaysBetweenSms='{self.DaysBetweenSms}'")
    
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
