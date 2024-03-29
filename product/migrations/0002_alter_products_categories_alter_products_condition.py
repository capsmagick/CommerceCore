# Generated by Django 4.2.4 on 2024-03-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("masterdata", "0001_initial"),
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="categories",
            field=models.ManyToManyField(
                related_name="product_categories",
                to="masterdata.category",
                verbose_name="Category",
            ),
        ),
        migrations.AlterField(
            model_name="products",
            name="condition",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Condition"
            ),
        ),
    ]
