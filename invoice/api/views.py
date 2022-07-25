import stripe
import bitly_api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from invoice.models import Invoice
from invoice.api.serializers import InvoiceSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
#bitly access token
access_toekn = "e663e30818201d28dd07803e57333bed4f15803a"


def shorten(checkout_session_url):
    connection = bitly_api.Connection(access_token=access_toekn)
    checkout_session_url = connection.shorten(checkout_session_url)
    # print(checkout_session_url)
    return checkout_session_url.get('url')


class InvoiceAPIView(APIView):
    """
        List all invoices, or create a new invoice.
    """
    def get(self, request):
        data = Invoice.objects.all()
        serializer = InvoiceSerializer(data, many=True)
        return Response(serializer.data)
    """
    {
    "name" : "one",
    "email" : "one@gmail.com",
    "project_name" : "ones project",
    "amount" : "1000.00"
    }
    """
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
post url   /create-payment/
payload data   {"invoice_number":1}
"""

class StripAPIView(APIView):
    def post(self, request):
        invoice_number = request.data.get("invoice_number")
        data = Invoice.objects.get(invoice_number=invoice_number)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        # 'price': '{{PRICE_ID}}',
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': data.amount,
                            'product_data': {
                                'name': data.name,
                                'email': data.email,
                                'project_name': data.project_name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id{CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            # return redirect(checkout_session.url)
            checkout_session_url = checkout_session.url
            checkout_session_url = shorten(checkout_session_url)

            # send_mail

            subject = "Invoice Link"
            html_content = '<p>' + data.name + '</p>' + '<p>' + str(data.amount) + '</p>' + \
                           '<p>' + data.project_name + '</p>' + '<p>' + str(checkout_session_url) + '</p>'
            send_mail(subject, html_content, 'from@example.com', [data.email], fail_silently=False,)
            return redirect(checkout_session.url)

        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


