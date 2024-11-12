import random
import uuid

from math import floor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from app.models import Account

"""
This simple CRUD application performs the following operations sequentially:
    1. Creates 100 new accounts with randomly generated IDs and randomly-computed balance amounts.
    2. Chooses two accounts at random and takes half of the money from the first and deposits it
     into the second.
    3. Chooses five accounts at random and deletes them.
"""

SEEN_ACCOUNT_IDS = []


def create_accounts(session, num: int) -> None:
    """
    Create N new accounts with random account IDs and account balances.
    """

    print("Creating new accounts...")

    counter = num
    new_accounts = []

    while counter > 0:
        account_id = uuid.uuid4()
        account_balance = floor(random.random() * 1_000_000)
        new_accounts.append(Account(id=account_id, balance=account_balance))
        SEEN_ACCOUNT_IDS.append(account_id)

        print(f"Created new account with id {account_id} and balance {account_balance}.")

        counter -= 1

    session.add_all(new_accounts)

def transfer_funds_randomly(session, first: uuid, second: uuid) -> None:
    """
    Transfer money randomly between two accounts.
    """

    try:
        source = session.query(Account).filter(Account.id == first).one()
        destination = session.query(Account).filter(Account.id == second).one()
    except NoResultFound:
        print("Accounts was not found")
        return None
    except MultipleResultsFound:
        raise ValueError(f"DB error: multiple results were found: {first} or {second}")

    amount = floor(source.balance/2)
    if 0 < source.balance < amount:
        raise ValueError(f"Insufficient funds in account {first}")

    print(f"\nTransferring {amount} from account {first} to account {second}...")
    source.balance -= amount
    destination.balance += amount

    print(f"Transfer complete.\nNew balances:\n\tAccount {first}: {source.balance}\n\tAccount {second}: {destination.balance}")


def delete_accounts(session, num):
    """
    Delete N existing accounts, at random.
    """

    counter = num
    to_delete_ids = []

    print("\nDeleting existing accounts...")
    while counter > 0:
        id_to_delete = random.choice(SEEN_ACCOUNT_IDS)

        if id_to_delete not in to_delete_ids:
            to_delete_ids.append(id_to_delete)
            counter -= 1

    accounts = session.query(Account).filter(Account.id.in_(to_delete_ids)).all()

    for account in accounts:
        print(f"Deleted account {account.id}.")
        SEEN_ACCOUNT_IDS.remove(account.id)
        session.delete(account)


if __name__ == '__main__':
    db_url = r'cockroachdb://root:admin@127.0.0.1:26257/defaultdb'

    try:
        engine = create_engine(db_url, connect_args={"application_name":"docs_simplecrud_sqlalchemy"})

        run_transaction(sessionmaker(bind=engine),
                        lambda s: create_accounts(s, 10))

        from_id = random.choice(SEEN_ACCOUNT_IDS)
        to_id = random.choice([id for id in SEEN_ACCOUNT_IDS if id != from_id])

        run_transaction(sessionmaker(bind=engine),
                        lambda s: transfer_funds_randomly(s, from_id, to_id))

        run_transaction(sessionmaker(bind=engine),
                                     lambda s: delete_accounts(s, 5))

    except Exception as e:
        print("Failed to connect to database.")
        print(f"{e}")
