import schedule
import time
import threading


def start_scheduler():
    from .jobs import check_preorders
    """
    Start the scheduler in a separate thread to avoid blocking the main Django process.
    """
    # Schedule the job to run every minute
    schedule.every(15).seconds.do(check_preorders)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Start the scheduler in a background thread
    thread = threading.Thread(target=run_scheduler)
    thread.daemon = True  # This ensures the thread will exit when the main process exits
    thread.start()
