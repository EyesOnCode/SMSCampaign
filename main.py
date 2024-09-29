from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.customer import Customer
from models.campaign import Campaign
from models.sms import SMS

# Replace with your actual database credentials
DATABASE_URI = 'mysql+pymysql://smolny1:EyesOn2ndCode!@localhost/customer_relations'

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def add_customers():
    # Create new customer instances
    customer1 = Customer(Name='Anna Nowak', Gender='Female', Title='Pani', Wolacz='Anno', Phone='+48 506 976 368')
    customer2 = Customer(Name='Piotr Kowalski', Gender='Male', Title='Pan', Wolacz='Piotrze', Phone='+48 730 257 469')
    customer3 = Customer(Name='Maria Wiśniewska', Gender='Female', Title='Pani', Wolacz='Mario', Phone='+48 536 386 919')
    customer4 = Customer(Name='Tomasz Zieliński', Gender='Male', Title='Pan', Wolacz='Tomaszu', Phone='+48 537 075 651')
    customer5 = Customer(Name='Katarzyna Wójcik', Gender='Female', Title='Pani', Wolacz='Katarzyno', Phone='+48 536 980 174')
    customer6 = Customer(Name='Jan Kaczmarek', Gender='Male', Title='Pan', Wolacz='Janie', Phone='+48 506 976 368')
    customer7 = Customer(Name='Ewa Mazur', Gender='Female', Title='Pani', Wolacz='Ewo', Phone='+48 730 257 469')
    customer8 = Customer(Name='Michał Dąbrowski', Gender='Male', Title='Pan', Wolacz='Michale', Phone='+48 536 386 919')
    customer9 = Customer(Name='Agnieszka Lewandowska', Gender='Female', Title='Pani', Wolacz='Agnieszko', Phone='+48 537 075 651')
    customer10 = Customer(Name='Grzegorz Kamiński', Gender='Male', Title='Pan', Wolacz='Grzegorzu', Phone='+48 536 980 174')




    # Add customers to the session
    session.add(customer1)
    session.add(customer2)
    session.add(customer3)
    session.add(customer4)
    session.add(customer5)
    session.add(customer6)
    session.add(customer7)
    session.add(customer8)
    session.add(customer9)
    session.add(customer10)


    # Commit the session to save changes to the database
    session.commit()
    print(f"Added customers: {customer1}, {customer2}")

if __name__ == "__main__":
    add_customers()
    session.close()
