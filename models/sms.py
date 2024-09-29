from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

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
