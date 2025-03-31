# 7. Backend Jobs

# a. Scheduled Job - Daily reminders - The application should send daily reminders to service professionals on g-chat using Google Chat Webhooks or SMS or mail

#     Check if a professional has not visited/has pending service request
#     If yes, then send the alert asking them to visit/accept/reject the service request
#     The reminder can be sent in the evening, every day (students can choose the time)

# b. Scheduled Job - Monthly Activity Report - Devise a monthly report for the customer created using HTML and sent via mail.

#     The activity report can include service details, how many services were requested/closed etc.
#     For the monthly report to be sent, start a job on the first day of every month → create a report using the above parameters → send it as an email

from workers import celery
from models import *
from celery.schedules import crontab
from mailer import send_email
from datetime import datetime
from flask import render_template

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test_celery every minute.
    sender.add_periodic_task(crontab(minute='*/1'), scheduled_job_daily_reminders.s())

@celery.task()
def scheduled_job_daily_reminders():
    #send mail to professionals to view pending service requests
    professionals=Professionals.query.all()

    for professional in professionals:
        pending_reqs=Servicerequest.query.filter_by(profesid=professional.id).filter_by(status='pending').all()

        if pending_reqs:
            body=f'Hello {professional.users.name}! you have {len(pending_reqs)} pending service requests.'
            send_email(subject='Pending Service Requests', to=professional.users.email, body=body)
            return f'mail sent to {professional.id} for pending service requests'
