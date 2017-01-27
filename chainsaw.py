#!/usr/bin/python3

# import sqlite3
# import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from juggler import Juggler

engine = create_engine("sqlite:///chainsaw.sqlite", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def setup_database():

        Juggler.create_tables()

        # Test if table is empty and seed it as needed

        juggler = session.query(Juggler).first()

        if juggler is None:
            print("Empty table, seeding...")
            # populate the table with some starter entries
            seed_data = (
                ("Ian Stewart", "Canada", 94),
                ("Aaron Gregg", "Canada", 88),
                ("Chad Taylor", "USA", 78)
            )
            for entry in seed_data:
                juggler = Juggler(
                    name=entry[0],
                    country=entry[1],
                    num_tries=entry[2]
                )
                session.add(juggler)

            session.commit()
        else:
            print("Table not empty, proceeding...")


def show_menu():
    print("""
    1. Show table
    2. Add record
    3. Update record
    4. Delete record
    0. Quit
    """)


def get_choice():
    while True:
        choice = int(input("Please enter on option: "))
        if 0 <= choice <= 4:
            return choice
        else:
            print("Please enter a valid option!")


def show_table():
    for juggler in session.query(Juggler):
        print(juggler)


def add_record():

    name = input("Enter the name of the person: ")
    country = input("Enter the country of the person: ")
    catches = input("Enter the number of catches for the record: ")
    catches_int = int(catches)  # TODO more robust validation

    juggler = Juggler(
        name=name,
        country=country,
        num_tries=catches_int
    )

    session.add(juggler)
    session.commit()
    print("Record added")


def update_record():

    # First loop until we get a valid person
    # TODO: We should really dump back to main menu if query fails
    while True:
        name_query = input("Whose record would you like to update? ")
        # Pad with wildcards for LIKE
        substr_query = '%' + name_query + '%'

        juggler = session.query(Juggler).filter(
            Juggler.name.like(substr_query)
        ).first()  # get the first matching query

        if juggler is None:
            print("Can't find anyone with that name...")
            continue  # prompt for name again
        else:
            y_or_n = input("Do you mean \"" + juggler.name + "\"? [Y/N] ")
            if y_or_n.upper() == "N":
                continue
            else:  # default case so we can quickly Enter through prompt
                break

    # having selected a record, we can continue
    print(juggler.name + "\'s best record is currently " +
          str(juggler.num_tries))
    new_catches = input("Enter an updated record: ")
    new_catches_int = int(new_catches)  # TODO better input validation

    # update the value in the object
    juggler.num_tries = new_catches_int

    # ORM automatically performs update?
    session.commit()


def delete_record():

    # First loop until we get a valid person
    # TODO: We should really dump back to main menu if query fails
    while True:
        name_query = input("Whose record would you like to delete? ")
        # Pad with wildcards for LIKE
        substr_query = '%' + name_query + '%'

        juggler = session.query(Juggler).filter(
            Juggler.name.like(substr_query)
        ).first()  # get the first matching query

        if juggler is None:
            print("Can't find anyone with that name...")
            continue  # prompt for name again
        else:
            y_or_n = input("Do you mean \"" + juggler.name + "\"? [Y/N] ")
            if y_or_n.upper() == "N":
                continue
            else:  # default case so we can quickly Enter through prompt
                break

    # having selected a record, we can continue
    print("Deleting " + juggler.name + "...")

    session.delete(juggler)
    session.commit()


def main():
    setup_database()
    while True:
        show_menu()
        choice = get_choice()
        if choice == 1:
            show_table()
        elif choice == 2:
            add_record()
        elif choice == 3:
            update_record()
        elif choice == 4:
            delete_record()
        else:
            # Selected quit
            session.close()
            break

main()
