# Generated by Django 4.2.7 on 2024-02-03 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asset_master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=100, null=True)),
                ('completed_orders', models.CharField(blank=True, max_length=100, null=True)),
                ('deployed_order', models.CharField(blank=True, max_length=100, null=True)),
                ('taxed', models.CharField(blank=True, max_length=100, null=True)),
                ('email_address', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_revenue', models.CharField(blank=True, max_length=100, null=True)),
                ('commercial_address', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateField(blank=True, default=None, null=True)),
                ('secondary_email', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('order_status', models.IntegerField(choices=[(1, 'Booked'), (2, 'Approved'), (3, 'Cancelled')], default=1)),
                ('organization', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('customer', models.CharField(blank=True, max_length=100, null=True)),
                ('deployment_date', models.DateField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('name_of_consignee', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=100, null=True)),
                ('mode_of_dispatch', models.CharField(blank=True, max_length=100, null=True)),
                ('transportation', models.CharField(blank=True, max_length=100, null=True)),
                ('order_to', models.CharField(blank=True, max_length=100, null=True)),
                ('order_from', models.CharField(blank=True, max_length=100, null=True)),
                ('out_date_and_time', models.DateField(blank=True, null=True)),
                ('prepared_by_name', models.CharField(blank=True, max_length=100, null=True)),
                ('prepared_by_email', models.CharField(blank=True, max_length=100, null=True)),
                ('poc_at_venue_name', models.CharField(blank=True, max_length=100, null=True)),
                ('poc_at_venue_email', models.CharField(blank=True, max_length=100, null=True)),
                ('truck_details', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_details', models.CharField(blank=True, max_length=100, null=True)),
                ('driver_details', models.CharField(blank=True, max_length=100, null=True)),
                ('purpose', models.CharField(blank=True, max_length=100, null=True)),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('office_address', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('challan_number', models.CharField(blank=True, max_length=100, null=True)),
                ('approve_order', models.BooleanField(default=False)),
                ('order_dispatch', models.BooleanField(default=False)),
                ('assets', models.ManyToManyField(blank=True, related_name='order_details', to='asset_master.assetmaster')),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.customerdetail')),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.IntegerField(blank=True, null=True)),
                ('customer', models.CharField(blank=True, max_length=100, null=True)),
                ('completed_orders', models.CharField(blank=True, max_length=100, null=True)),
                ('deployed_order', models.CharField(blank=True, max_length=100, null=True)),
                ('taxed', models.CharField(blank=True, max_length=100, null=True)),
                ('email_address', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_revenue', models.CharField(blank=True, max_length=100, null=True)),
                ('commercial_address', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateField(blank=True, default=None, null=True)),
                ('secondary_email', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderdetail')),
            ],
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('date_time', models.DateTimeField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderdetail')),
            ],
        ),
        migrations.CreateModel(
            name='OrderAttachFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attached_file', models.FileField(blank=True, default=None, null=True, upload_to='media/')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderdetail')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('date_time', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.customerdetail')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAttachFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attached_file', models.FileField(blank=True, default=None, null=True, upload_to='media/')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.customerdetail')),
            ],
        ),
    ]
