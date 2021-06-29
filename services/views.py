from rest_framework import generics
from services.models import Company, TypeOfService
from services.permissions import IsOwner
from services.serializers import CompanySerializer, DetailCompanySerializer, TypeOfServiceCreateSerializer, \
    TypeOfServiceDetailSerializer
from services.services_logic import save_information_about_user_employee_position_in_type_of_services, \
    get_company_where_user_consist_in_type_of_service
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CompanyCreateView(generics.CreateAPIView):
    """Creates Company"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CompaniesListView(generics.ListAPIView):
    """The list of companies in which the user participates"""
    serializer_class = CompanySerializer

    def get_queryset(self, *args, **kwargs):
        return get_company_where_user_consist_in_type_of_service(user=self.request.user)
    permission_classes = [IsAuthenticatedOrReadOnly]


class CompanyRetrieveView(generics.RetrieveAPIView):
    """Company details"""
    queryset = Company.objects.all()
    serializer_class = DetailCompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TypeOfServiceCreateView(generics.CreateAPIView):
    """Creates TypeOfService"""
    queryset = TypeOfService.objects.all()
    serializer_class = TypeOfServiceCreateSerializer

    def perform_create(self, serializer):
        save_information_about_user_employee_position_in_type_of_services(serializer=serializer,
                                                                          user=self.request.user,
                                                                          employee_position="A")


class TypeOfServiceDetailView(generics.RetrieveAPIView):
    """TypeOfService details"""
    queryset = TypeOfService.objects.all()
    serializer_class = TypeOfServiceDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CompanyUpdateView(generics.UpdateAPIView):
    """Updates Company"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsOwner]


