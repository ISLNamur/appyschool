# Generated by Django 2.0.9 on 2019-05-28 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_importcalendarmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsiblemodel',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='birth date'),
        ),
    ]
