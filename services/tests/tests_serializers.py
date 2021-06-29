from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from services.models import Company, TypeOfService, Membership
from services.serializers import CompanySerializer, CompanyInformationSerializer, DetailCompanySerializer, \
    MembershipsSerializer, TypeOfServiceDetailSerializer, TypeOfServiceSerializer

User = get_user_model()


class ServicesSerializerTestCase(TestCase):
    def test_serializers(self):
        user = User.objects.create(username='TestUser',
                                   email='test@gmail.com',
                                   password='password')
        company1 = Company.objects.create(name='Test Company1',
                                          description='Test description 1',
                                          owner=user)
        company2 = Company.objects.create(name='Test Company2',
                                          description='Test description 2',
                                          owner=user)
        type_of_service1 = TypeOfService.objects.create(company=company1,
                                                        name='Test TypeOfService 1')
        type_of_service2 = TypeOfService.objects.create(company=company1,
                                                        name='Test TypeOfService 2')
        membership1 = Membership.objects.create(user=user,
                                                types_of_service=type_of_service1,
                                                employee_position='A')
        membership2 = Membership.objects.create(user=user,
                                                types_of_service=type_of_service2,
                                                employee_position='M')

        expected_data1 = [
            {
                'id': 1,
                'name': 'Test Company1',
                'description': 'Test description 1',
                'owner': 1
            },
            {
                'id': 2,
                'name': 'Test Company2',
                'description': 'Test description 2',
                'owner': 1
            }
        ]
        serializer1 = CompanySerializer([company1, company2], many=True).data
        self.assertEqual(expected_data1, serializer1)

        expected_data2 = [
            {
                'id': 1,
                'name': 'Test Company1'
            },
            {
                'id': 2,
                'name': 'Test Company2',
            }
        ]
        serializer2 = CompanyInformationSerializer([company1, company2], many=True).data
        self.assertEqual(expected_data2, serializer2)

        factory = RequestFactory()
        request = factory.get('')
        request.user = user
        context = {"request": request}

        expected_data3 = {
            'id': 1,
            'type_of_services': [
                {
                    'id': 1,
                    'name': 'Test TypeOfService 1',
                },
                {
                    'id': 2,
                    'name': 'Test TypeOfService 2'
                }
            ],
            'name': 'Test Company1',
            'description': 'Test description 1',
            'owner': 1
        }

        serializer3 = DetailCompanySerializer(company1, context=context).data
        self.assertEqual(serializer3, expected_data3)

        expected_data4 = [
            {
                'employee_position': 'Administrator'
            },
            {
                'employee_position': 'Master'
            }
        ]
        serializer4 = MembershipsSerializer([membership1, membership2], many=True).data
        self.assertEqual(serializer4, expected_data4)

        expected_data5 = {
            'id': 1,
            'name': 'Test TypeOfService 1',
            'company': {
                'id': 1,
                'name': 'Test Company1'
            },
            'employee_position': 'Administrator'
        }

        serializer5 = TypeOfServiceDetailSerializer(type_of_service1, context=context).data
        self.assertEqual(serializer5, expected_data5)

        expected_data6 = {
            'id': 1,
            'name': 'Test TypeOfService 1'
        }
        serializer6 = TypeOfServiceSerializer(type_of_service1, context=context).data
        self.assertEqual(serializer6,  expected_data6)
