# Generated by Django 4.2.4 on 2024-03-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0004_return"),
    ]

    operations = [
        migrations.AddField(
            model_name="return",
            name="return_id",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Return Id"
            ),
        ),
        migrations.AlterField(
            model_name="return",
            name="refund_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Pending", "Pending"),
                    ("In Transit", "In Transit"),
                    ("Delivered", "Delivered"),
                    ("Refund Initiated", "Refund Initiated"),
                    ("Refunded", "Refunded"),
                ],
                max_length=25,
                null=True,
                verbose_name="Refund Status",
            ),
        ),
    ]
