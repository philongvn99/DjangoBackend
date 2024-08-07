# Generated by Django 4.2.13 on 2024-07-22 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Team", "0002_auto_20240721_2159"),
    ]

    operations = [
        migrations.AddField(
            model_name="league",
            name="acronym_name",
            field=models.CharField(
                blank=True, db_column="str_acronym_name", max_length=50, null=True
            ),
        ),
        migrations.AddField(
            model_name="league",
            name="logo_link",
            field=models.CharField(
                blank=True, db_column="str_logo_link", max_length=50, null=True
            ),
        ),
    ]
