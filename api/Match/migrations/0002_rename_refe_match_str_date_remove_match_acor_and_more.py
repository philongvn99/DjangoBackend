# Generated by Django 4.2.13 on 2024-07-22 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Match", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="match",
            old_name="refe",
            new_name="str_date",
        ),
        migrations.RemoveField(
            model_name="match",
            name="acor",
        ),
        migrations.RemoveField(
            model_name="match",
            name="afou",
        ),
        migrations.RemoveField(
            model_name="match",
            name="arca",
        ),
        migrations.RemoveField(
            model_name="match",
            name="asht",
        ),
        migrations.RemoveField(
            model_name="match",
            name="asot",
        ),
        migrations.RemoveField(
            model_name="match",
            name="ayca",
        ),
        migrations.RemoveField(
            model_name="match",
            name="hcor",
        ),
        migrations.RemoveField(
            model_name="match",
            name="hfou",
        ),
        migrations.RemoveField(
            model_name="match",
            name="hrca",
        ),
        migrations.RemoveField(
            model_name="match",
            name="hsht",
        ),
        migrations.RemoveField(
            model_name="match",
            name="hsot",
        ),
        migrations.RemoveField(
            model_name="match",
            name="hyca",
        ),
    ]
