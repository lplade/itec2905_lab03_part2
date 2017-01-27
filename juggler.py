from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///chainsaw.sqlite", echo=True)


class Juggler(Base):
    """
    Defines metadata about a juggler table.
    Will create Juggler objects from rows in this table.
    """

    __tablename__ = "Juggler"

    # map table to object
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String)
    num_tries = Column(Integer, nullable=False)

    # TODO write __str__ for columnar output

    def __repr__(self):
        """

        :return:
        """
        return "Juggler: name = {} country = {} record = {}".format(
            self.name, self.country, self.num_tries
        )

    @staticmethod
    def create_tables():
        """
        Invoke this upon initialization to set up tables
        :return:
        """
        Base.metadata.create_all(engine)


