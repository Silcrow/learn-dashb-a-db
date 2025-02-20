# app.py
from dao import FetchDAO
from database import SessionLocal


def main():
    session = SessionLocal()
    try:
        # Fetch and display sample data
        FetchDAO.fetch_data(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
