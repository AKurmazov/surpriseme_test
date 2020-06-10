from django import forms

from payouts.models import Payout


class PayoutForm(forms.ModelForm):
    class Meta:
        model = Payout
        fields = ('amount', 'account_number',)
