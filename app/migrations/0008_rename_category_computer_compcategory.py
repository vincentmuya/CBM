# Generated by Django 3.2.7 on 2021-10-11 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20211011_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer',
            old_name='category',
            new_name='compcategory',
        ),
    ]
