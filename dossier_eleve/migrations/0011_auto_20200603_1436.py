# Generated by Django 2.2.11 on 2020-06-03 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dossier_eleve', '0010_auto_20200512_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caseleve',
            options={'permissions': (('set_sanction', 'Can set sanction'), ('ask_sanction', 'Can ask sanction'))},
        ),
    ]
