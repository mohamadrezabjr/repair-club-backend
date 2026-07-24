from django.urls import path
from accounting_app.views.transaction import (
    TransactionListCreateAPIView,
    TransactionRetrieveUpdateDestroyAPIView,
    TransactionCategoryListCreateAPIView,
    TransactionCategoryRetrieveUpdateDestroyAPIView,
)
from accounting_app.views.cheque import (
    ChequeListCreateAPIView,
    ChequeRetrieveUpdateDestroyAPIView,
)
from accounting_app.views.report import AccountingSummaryAPIView

urlpatterns = [
    path('reports/summary/', AccountingSummaryAPIView.as_view(), name='accounting-summary'),

    path('transactions/', TransactionListCreateAPIView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyAPIView.as_view(), name='transaction-detail'),

    path('categories/', TransactionCategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', TransactionCategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),

    path('cheques/', ChequeListCreateAPIView.as_view(), name='cheque-list'),
    path('cheques/<int:pk>/', ChequeRetrieveUpdateDestroyAPIView.as_view(), name='cheque-detail'),
]
