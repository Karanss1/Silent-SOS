from django.urls import path
from .views import ChatbotResponseView

urlpatterns = [
    path('response/', ChatbotResponseView.as_view(), name='chatbot-response'),
]
