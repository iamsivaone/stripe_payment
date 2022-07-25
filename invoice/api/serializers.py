from rest_framework import serializers
from invoice.models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['invoice_number', 'name', 'email', 'project_name', 'amount']
