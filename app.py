from dao import FetchDAO
from database import SessionLocal
from dashboard import app
import threading


def main():
    session = SessionLocal()
    try:
        # Fetch and display sample data
        FetchDAO.fetch_data(session)
    finally:
        session.close()


def run_dash():
    # Start the Dash app in a separate thread
    app.run_server(debug=True, use_reloader=False)  # `use_reloader=False` to avoid running twice


if __name__ == "__main__":
    # Run both the Dash app and FetchDAO logic concurrently
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.start()

    # Run the original main logic (FetchDAO)
    main()

    # Ensure the Dash app keeps running in the background
    dash_thread.join()
