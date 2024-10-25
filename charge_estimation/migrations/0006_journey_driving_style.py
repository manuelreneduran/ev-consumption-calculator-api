# Generated by Django 5.1.2 on 2024-10-25 21:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("charge_estimation", "0005_journey_percentage_charge_used_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="journey",
            name="driving_style",
            field=models.CharField(
                choices=[
                    ("VERY_EFFICIENT", 0.75),
                    ("EFFICIENT", 0.9),
                    ("REGULAR", 1.0),
                    ("AGGRESSIVE", 1.3043),
                    ("VERY_AGGRESSIVE", 1.5),
                ],
                default="REGULAR",
                max_length=20,
            ),
        ),
    ]