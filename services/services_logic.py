from django.db.models import Q
from services.models import Membership, Company
from django.contrib.auth import get_user_model

User = get_user_model()


def save_information_about_user_employee_position_in_type_of_services(serializer, user: User,employee_position: str):
    """Saves information about the user's employee position in the type of services"""
    obj = serializer.save()
    membership = Membership(user=user,
                            types_of_service=obj,
                            employee_position=employee_position)
    membership.save()


def get_company_where_user_consist_in_type_of_service(user: User):
    """Returns a list of companies whose types of service the user is a member of"""
    return Company.objects.filter(Q(type_of_services__memberships__user=user)
                                  | Q(owner=user))
