from django.contrib.auth import get_user_model
from rest_framework import serializers
from services.models import Company, TypeOfService, Membership

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class FilteredTypeOfServiceSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(memberships__user=self.context['request'].user)
        return super(FilteredTypeOfServiceSerializer, self).to_representation(data)


class MembershipsSerializer(serializers.ModelSerializer):
    employee_position = serializers.CharField(source='get_employee_position_display')

    class Meta:
        model = Membership
        fields = ('employee_position', )


class TypeOfServiceSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredTypeOfServiceSerializer
        model = TypeOfService
        fields = ('id', 'name', )


class TypeOfServiceDetailSerializer(serializers.ModelSerializer):
    company = CompanyInformationSerializer()
    employee_position = serializers.SerializerMethodField()

    def get_employee_position(self, obj):
        return obj.memberships.get(user=self.context['request'].user).get_employee_position_display()

    class Meta:
        list_serializer_class = FilteredTypeOfServiceSerializer
        model = TypeOfService
        fields = ('id', 'name', 'company', 'employee_position', )


class TypeOfServiceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfService
        exclude = ('code', )


class DetailCompanySerializer(CompanySerializer):
    type_of_services = TypeOfServiceSerializer(many=True)
