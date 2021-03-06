# Generated by Django 3.2.4 on 2021-06-18 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название компании')),
                ('description', models.TextField(verbose_name='Описание компании')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_position', models.CharField(choices=[('M', 'Master'), ('A', 'Administrator')], default='M', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название типа услуги')),
                ('code', models.CharField(max_length=10, verbose_name='Код для вступления')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_of_services', to='services.company', verbose_name='Компания')),
                ('members', models.ManyToManyField(through='services.Membership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название услуги')),
                ('price', models.FloatField(verbose_name='Цена услуги')),
                ('types_of_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.typeofservice', verbose_name='Тип услуги')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='types_of_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.typeofservice'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя мастера')),
                ('types_of_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masters', to='services.typeofservice', verbose_name='Тип услуги')),
            ],
        ),
    ]
