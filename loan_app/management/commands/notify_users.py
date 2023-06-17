from datetime import timedelta
from django.core.management.base import BaseCommand
from loan_app.models import Loan
from django.utils import timezone


class Command(BaseCommand):
    help = 'Send reminder emails to users 2 days before'

    def handle(self, *args, **kwargs):
        loans = Loan.objects.filter(
            due_date__date=timezone.datetime.now() + timedelta(days=2),
            status='APPROVED',
        )
        for loan in loans:
            # Send reminder email to this email
            user_email = loan.user_account.user.email
        self.stdout.write(user_email)
