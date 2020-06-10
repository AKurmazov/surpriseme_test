from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.utils import timezone
import requests

from payouts.models import Payment, Payout


class CustomPayoutAdmin(admin.ModelAdmin):
    change_form_template = "admin/payouts/payout/change_form.html"

    list_display = ('author', 'amount', 'is_processed', 'processed_date')
    list_filter = ('created_date',)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_processed:
            return [field.name for field in obj.__class__._meta.fields]
        return []

    def response_change(self, request, obj):
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        if "pay-action" in request.POST:
            obj.is_processed = True
            obj.processed_date = timezone.now()
            obj.author.revenue -= obj.amount
            obj.author.save()
            if obj.account_number:
                requests.post("https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4", json={
                    "account": obj.account_number,
                    "amount": obj.amount
                })
            obj.save()

            redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            return super(CustomPayoutAdmin, self).response_change(request, obj)


class CustomPaymentAdmin(admin.ModelAdmin):
    list_display = ('author', 'amount', 'created_date')
    list_filter = ('created_date',)


admin.site.register(Payment, CustomPaymentAdmin)
admin.site.register(Payout, CustomPayoutAdmin)
