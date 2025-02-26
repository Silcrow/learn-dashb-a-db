from database.dao import FetchDAO
from database.database import SessionLocal
from dashboard.dashboard import app
import threading
import time


def main():
    """ Main logic: FetchDAO-related operations. """
    session = SessionLocal()
    try:
        FetchDAO.fetch_data(session)
    finally:
        session.close()


def run_dash():
    """ Run the Dash app. """
    app.run_server(debug=True, use_reloader=False)  # `use_reloader=False` prevents duplicate execution


if __name__ == "__main__":
    # Start Dash in a daemon thread, so it stops when the script exits
    run_dash()
    # dash_thread = threading.Thread(target=run_dash, daemon=True)
    # dash_thread.start()
    #
    # try:
    #     main()  # Run FetchDAO logic
    #     while True:  # Keep the main thread alive
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("\nShutting down gracefully...")
