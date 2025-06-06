# Generated by Django 5.0.3 on 2025-05-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanresult',
            name='fhir_observation_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='scanresult',
            name='fhir_patient_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='scanresult',
            name='file_name',
            field=models.CharField(max_length=200),
        ),
    ]
