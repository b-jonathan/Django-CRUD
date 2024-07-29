# Generated by Django 4.2.3 on 2023-07-26 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qc', '0004_alter_employee_options_alter_member_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplainCategory',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('complain_category', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'complain_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InternalComplainDetails',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ic_id', models.IntegerField(db_column='IC_id', db_comment='foreign key')),
                ('produce_id', models.IntegerField(db_comment='product yg dicomplain')),
                ('process_name', models.CharField(max_length=25)),
                ('complain_category', models.SmallIntegerField(db_comment='another table')),
                ('complain_description', models.TextField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'internal_complain_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InternalComplainTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.IntegerField(db_comment='customer who complains')),
                ('nomor_document', models.CharField(db_comment='nomor IC', max_length=200)),
                ('document_date', models.DateField(db_comment='tanggal IC')),
                ('created_by', models.CharField(max_length=30)),
                ('created_date', models.DateField(blank=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=30, null=True)),
                ('updated_date', models.DateField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'internal_complain_table',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='employee',
            table='employee',
        ),
        migrations.AlterModelTable(
            name='member',
            table='member',
        ),
    ]
