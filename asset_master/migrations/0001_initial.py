# Generated by Django 4.2.7 on 2024-02-03 01:04

import asset_master.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('fc_no', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_category', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('model_no', models.CharField(blank=True, max_length=100, null=True)),
                ('serial_no', models.CharField(blank=True, max_length=100, null=True)),
                ('sku', models.CharField(blank=True, max_length=100, null=True)),
                ('asset_tag', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.CharField(blank=True, max_length=100, null=True)),
                ('box_number', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('last_service_date', models.DateField(blank=True, default=None, null=True)),
                ('upcoming_service_date', models.DateField(blank=True, default=None, null=True)),
                ('length', models.CharField(blank=True, max_length=100, null=True)),
                ('breadth', models.CharField(blank=True, max_length=100, null=True)),
                ('height', models.CharField(blank=True, max_length=100, null=True)),
                ('width', models.CharField(blank=True, max_length=100, null=True)),
                ('warranty_period', models.CharField(blank=True, max_length=100, null=True)),
                ('under_amc', models.BooleanField(default=False)),
                ('amc_date', models.DateField(blank=True, null=True)),
                ('storage_warehouse_number', models.CharField(blank=True, max_length=100, null=True)),
                ('availability', models.BooleanField(default=False)),
                ('outward_date', models.DateField(blank=True, null=True)),
                ('outward_remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('inward_date', models.DateField(blank=True, null=True)),
                ('inward_remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('vendor', models.CharField(blank=True, max_length=100, null=True)),
                ('purchased_on', models.DateField(blank=True, null=True)),
                ('cost_price', models.CharField(blank=True, max_length=100, null=True)),
                ('tax_rate', models.CharField(blank=True, max_length=100, null=True)),
                ('depricated_value', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateField(blank=True, null=True)),
                ('rented_asset', models.BooleanField(default=False)),
                ('rental_pricing', models.CharField(blank=True, max_length=100, null=True)),
                ('rent_collected', models.CharField(blank=True, max_length=100, null=True)),
                ('available_for_sale', models.CharField(blank=True, max_length=100, null=True)),
                ('asset_utilization', models.CharField(blank=True, max_length=100, null=True)),
                ('asset_status', models.CharField(blank=True, default='available', max_length=100, null=True)),
                ('repair_type', models.IntegerField(choices=[(10, 'Default Type'), (20, 'External Repair'), (30, 'Internal Repair')], default=10)),
                ('sold_asset', models.BooleanField(default=False)),
                ('loaned_asset', models.BooleanField(default=False)),
                ('loan_period', models.CharField(blank=True, max_length=100, null=True)),
                ('add_to_order', models.BooleanField(default=False)),
                ('confirm_order', models.BooleanField(default=False)),
                ('owner', models.CharField(blank=True, default='Zoom Communication', max_length=100, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='media/')),
            ],
        ),
        migrations.CreateModel(
            name='AssetMasterComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('asset_id', models.IntegerField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetMasterInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_transfer', models.IntegerField(choices=[(1, 'Send Transfer Request'), (2, 'Transfer Request Sent'), (3, 'Ready To Transfer'), (4, 'Transfered')], default=1)),
                ('move_to_inventory', models.BooleanField(default=False)),
                ('order_id', models.PositiveIntegerField(blank=True, null=True)),
                ('asset_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_master.assetmaster')),
            ],
        ),
        migrations.CreateModel(
            name='AssetMasterAttachFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attached_file', models.FileField(blank=True, default=None, null=True, upload_to='media/')),
                ('asset_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_master.assetmaster')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=200, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', asset_master.models.CustomUserManager()),
            ],
        ),
    ]
