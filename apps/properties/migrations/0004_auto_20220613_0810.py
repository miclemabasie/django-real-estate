# Generated by Django 3.2.7 on 2022-06-13 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_rename_propertyveiws_propertyviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='propertyviews',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
