# Generated by Django 2.0.1 on 2020-03-03 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qfauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]