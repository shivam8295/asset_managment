# Generated by Django 4.2.7 on 2024-03-20 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderdetail_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='poc_at_venue_email',
            new_name='maker_email',
        ),
    ]
