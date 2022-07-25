from django.urls import path

from invoice.api.views import InvoiceAPIView
from invoice.api.views import StripAPIView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('create-invoice/', InvoiceAPIView.as_view()),
    path('create-payment/', StripAPIView.as_view()),
]