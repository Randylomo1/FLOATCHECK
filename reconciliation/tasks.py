from celery import shared_task
from .logic import run_matching_engine

@shared_task(name="run_reconciliation_task")
def run_reconciliation_task():
    """
    A Celery task that triggers the main matching engine.
    This can be scheduled to run periodically or triggered on-demand.
    """
    print("Task `run_reconciliation_task` started.")
    try:
        run_matching_engine()
        print("Task `run_reconciliation_task` finished successfully.")
        return "Reconciliation task completed successfully."
    except Exception as e:
        # Log the exception for debugging
        print(f"ERROR in `run_reconciliation_task`: {e}")
        # You might want to use a more robust logging framework here
        # and potentially retry the task based on the error.
        raise
