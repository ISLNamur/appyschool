# Generated by Django 2.2.2 on 2019-06-18 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_responsiblemodel_birth_date'),
        ('student_absence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClasseNoteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True)),
                ('datetime_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date et heure de création de la note')),
                ('datetime_update', models.DateTimeField(auto_now=True, verbose_name='Date et heure de mise à jour de la note')),
                ('classe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.ClasseModel')),
            ],
        ),
    ]
