from celery import shared_task
from django.utils import timezone
from .models import DataRetentionPolicy
import logging

logger = logging.getLogger(__name__)

@shared_task
def enforce_data_retention_policies():
    """
    A Celery task that enforces all active data retention policies.
    """
    logger.info("Starting data retention policy enforcement...")
    active_policies = DataRetentionPolicy.objects.filter(is_active=True)

    if not active_policies.exists():
        logger.info("No active data retention policies found.")
        return

    for policy in active_policies:
        try:
            model_class = policy.content_type.model_class()
            retention_delta = timezone.timedelta(days=policy.retention_period_days)
            cutoff_date = timezone.now() - retention_delta

            # This assumes the model has a 'created_at' field. 
            # A more robust solution would allow specifying the timestamp field in the policy.
            if hasattr(model_class, 'created_at'):
                # Using _base_manager to include soft-deleted objects if applicable
                old_records = model_class._base_manager.filter(created_at__lt=cutoff_date)
                count = old_records.count()

                if count > 0:
                    old_records.delete()
                    logger.info(
                        f"Policy '{policy.name}': Deleted {count} records from "
                        f"{model_class.__name__} older than {policy.retention_period_days} days."
                    )
                else:
                    logger.info(
                        f"Policy '{policy.name}': No old records to delete from {model_class.__name__}."
                    )
            else:
                logger.warning(
                    f"Policy '{policy.name}': Model {model_class.__name__} does not have a 'created_at' field. "
                    f"Skipping."
                )
        except Exception as e:
            logger.error(f"Error enforcing policy '{policy.name}': {e}", exc_info=True)

    logger.info("Data retention policy enforcement finished.")
