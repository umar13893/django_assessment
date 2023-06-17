from django.contrib import admin
from .models import (
    UserAccount,
    Loan
)

# Register your models here.

admin.site.register(UserAccount)
admin.site.register(Loan)
