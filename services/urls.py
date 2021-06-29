from django.urls import path, include
from services import views

app_name = 'services'

urlpatterns = [
    path('create_company/', views.CompanyCreateView.as_view()),
    path('companies/', views.CompaniesListView.as_view()),
    path('company/<int:pk>', views.CompanyRetrieveView.as_view()),
    path('company_update/<int:pk>', views.CompanyUpdateView.as_view()),
    path('type_of_service_create/', views.TypeOfServiceCreateView.as_view()),
    path('type_of_service_detail/<int:pk>', views.TypeOfServiceDetailView.as_view()),
]