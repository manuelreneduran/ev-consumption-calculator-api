# Generated by Django 5.1.2 on 2024-10-25 21:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("charge_estimation", "0003_journey_ev_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="journey",
            old_name="estimated_charge_used_kwh",
            new_name="charge_used_kwh",
        ),
    ]
