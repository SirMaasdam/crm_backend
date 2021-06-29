from django.db import models
from django.contrib.auth import get_user_model
from services.logic import create_code
User = get_user_model()


class Company(models.Model):
    """Company Model"""
    name = models.CharField(verbose_name='Название компании',
                            max_length=255)
    description = models.TextField(verbose_name='Описание компании')
    owner = models.ForeignKey(User,
                              verbose_name='Создатель',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='companies')

    def __str__(self):
        return self.name


class TypeOfService(models.Model):
    """TypeOfService """
    company = models.ForeignKey(Company,
                                verbose_name='Компания',
                                on_delete=models.CASCADE,
                                related_name='type_of_services')
    members = models.ManyToManyField(User,
                                     through='Membership')
    name = models.CharField(verbose_name='Название типа услуги',
                            max_length=200)
    code = models.CharField(verbose_name='Код для вступления',
                            max_length=10)

    def save(self, *args, **kwargs):
        """Generates a unique code for the user to join the TypeOfService"""
        if not self.code:
            self.code = create_code(10)
        super().save(*args, **kwargs)


class Membership(models.Model):
    """
        The intermediary model linking the User and TypeOfService

        Contains information about the employee's position in TypeOfService
    """
    EMPLOYEE_POSITION = [
        ('M', 'Master'),
        ('A', 'Administrator')
    ]
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='memberships')
    types_of_service = models.ForeignKey(TypeOfService,
                                         on_delete=models.CASCADE,
                                         related_name='memberships')
    employee_position = models.CharField(choices=EMPLOYEE_POSITION,
                                         max_length=1,
                                         default='M')


class Service(models.Model):
    """Services provided in the TypeOfService"""
    types_of_service = models.ForeignKey(TypeOfService,
                                         verbose_name='Тип услуги',
                                         on_delete=models.CASCADE,
                                         related_name='services')
    name = models.CharField(verbose_name='Название услуги',
                            max_length=200)
    price = models.DecimalField(verbose_name='Цена услуги',
                                max_digits=7,
                                decimal_places=2)


class Master(models.Model):
    """A model for selecting the master who provides the service"""
    types_of_service = models.ForeignKey(TypeOfService,
                                         verbose_name='Тип услуги',
                                         on_delete=models.CASCADE,
                                         related_name='masters')
    name = models.CharField(verbose_name='Имя мастера',
                            max_length=200)

