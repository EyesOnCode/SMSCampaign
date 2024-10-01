from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
