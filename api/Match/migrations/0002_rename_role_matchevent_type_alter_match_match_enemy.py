# Generated by Django 4.2.13 on 2024-06-07 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Team", "0001_initial"),
        ("Match", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="matchevent",
            old_name="role",
            new_name="type",
        ),
        migrations.AlterField(
            model_name="match",
            name="match_enemy",
            field=models.ForeignKey(
                db_column="n4_enemy_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="Team.teamattendance",
            ),
        ),
    ]