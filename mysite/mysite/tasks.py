from celery import shared_task
from django.utils import timezone
from apps.rec.models import ScheduledReport
from apps.rec.tasks import send_scheduled_report

@shared_task
def check_scheduled_reports():
    """
    Checks for scheduled reports that are due to run and triggers them.
    """
    now = timezone.now()
    due_reports = ScheduledReport.objects.filter(next_run_at__lte=now)

    for report in due_reports:
        send_scheduled_report.delay(report.reconciliation.id, report.recipient_email)

        # Reschedule the report for the next run
        if report.frequency == 'daily':
            report.next_run_at += timezone.timedelta(days=1)
        elif report.frequency == 'weekly':
            report.next_run_at += timezone.timedelta(weeks=7)
        elif report.frequency == 'monthly':
            report.next_run_at += timezone.timedelta(days=30)
        report.save()
