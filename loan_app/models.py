from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


# Create your models here.


class UserAccount(models.Model):

    NON_MANAGERIAL = 'NON_MANAGERIAL'
    MANAGERIAL = 'MANAGERIAL'

    USER_TYPE = (
        (NON_MANAGERIAL, 'Non Managerial'),
        (MANAGERIAL, 'Managerial'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    user_type = models.CharField(max_length=255, choices=USER_TYPE, default=NON_MANAGERIAL)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"


@receiver(post_save, sender=User)
def user_account_create(sender, instance, created, **kwargs):
    if created:
        user_account = UserAccount(user=instance)
        user_account.save()
    else:
        pass


# Loans
class Loan(models.Model):

    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    LOAN_TYPES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )

    user_account = models.ForeignKey('UserAccount', on_delete=models.CASCADE, related_name='user_accounts')
    amount = models.IntegerField(default=0, verbose_name="Loan Amount")
    status = models.CharField(max_length=255, choices=LOAN_TYPES, default=PENDING, verbose_name="Status")
    due_date = models.DateTimeField(verbose_name="Due Date", default=datetime.datetime.now())
    comment = models.TextField(verbose_name="Comment", default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_account)

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"
