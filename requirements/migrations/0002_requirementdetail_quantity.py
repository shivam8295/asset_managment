# Generated by Django 4.2.7 on 2024-04-02 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requirements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirementdetail',
            name='quantity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
