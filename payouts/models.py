from django.db import models
from django.core.validators import MinValueValidator

from users.models import CustomUser


class Payment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="amount", validators=(MinValueValidator(0),))
    created_date = models.DateTimeField(verbose_name="created date", auto_now_add=True)

    def save(self, *args, **kwargs):
        self.author.revenue += 0.3 * self.amount
        self.author.save()
        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Payment #{self.pk} — {self.author} at {self.created_date}"


class Payout(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="amount", validators=(MinValueValidator(0),))
    is_processed = models.BooleanField(verbose_name="processed", default=False)
    account_number = models.TextField(verbose_name="account number", max_length=256, null=True, blank=True)
    created_date = models.DateTimeField(verbose_name="created date", auto_now_add=True)
    processed_date = models.DateTimeField(verbose_name="processed date", null=True, blank=True)

    def __str__(self):
        return f"Payout #{self.pk} - {self.author} at {self.created_date}"
