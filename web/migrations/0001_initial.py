# Generated by Django 3.2.4 on 2021-10-10 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('surname', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('email', models.CharField(max_length=255, verbose_name='Электронный адрес')),
                ('password', models.CharField(max_length=255, verbose_name='Пароль')),
            ],
        ),
    ]
