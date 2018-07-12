import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    f = open("zips.csv")
    reader = csv.reader(f)

    for zipcode, city, state, lat, long, population in reader:

        if len(str(zipcode)) == 4 :
            zipcode = str("0") + str(zipcode)
        db.execute("INSERT INTO zips (zipcode, city, state, lat, long, population) VALUES (:zipcode, :city, :state, :lat, :long, :population)",
                    {"zipcode": zipcode, "city": city, "state": state, "lat": lat, "long": long, "population": population})
        print(f"Added zipcode {zipcode} successfully.")

    db.commit()

if __name__ == "__main__":
    main()
