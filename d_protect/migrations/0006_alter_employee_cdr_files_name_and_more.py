# Generated by Django 4.2.14 on 2024-08-11 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d_protect', '0005_alter_employee_cdr_files_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='cdr_files_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='cdr_files_path',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='doct_file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='document_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
