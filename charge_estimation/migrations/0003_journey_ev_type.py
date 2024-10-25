# Generated by Django 5.1.2 on 2024-10-25 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "charge_estimation",
            "0002_remove_journey_destination_remove_journey_ev_type_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="journey",
            name="ev_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="charge_estimation.evtype",
            ),
        ),
    ]
