from sqlalchemy import create_engine, Table, Column, Integer, MetaData, Text


meta = MetaData()
engine = create_engine('sqlite:///site.db')


def main() -> None:
    reply = Table('Replys', meta,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('from', Integer, nullable=False, comment='User id reply sender'),
                  Column('content', Text, nullable=True),
                  Column('status', Text, nullable=True),
                  Column('doer', Integer, nullable=True),
                  Column('date', Text, nullable=True),
                  Column('level', Integer, nullable=True, comment='Level of access'),
                  )
    staff = Table('Staff', meta,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('prof', Text, nullable=True),
                  Column('level', Integer, nullable=True),
                  )
    users = Table('Users', meta,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('login', Text, nullable=False),
                  Column('pass', Text, nullable=False),
                  )
    logs = Table('Logs', meta,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('reply', Integer, nullable=False),
                 Column('worker', Integer, nullable=False),
                 Column('action', Text, nullable=False),
                 Column('old', Text, nullable=False),
                 Column('new', Text, nullable=False),
                 )
    meta.create_all(engine)


if __name__ == '__main__':
    main()
