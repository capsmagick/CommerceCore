# Generated by Django 4.2.4 on 2024-03-16 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("masterdata", "0003_brand_is_active_brand_tags"),
        ("product", "0003_collection_description_collection_feature_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="dimension",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="product_dimensions",
                to="masterdata.dimension",
                verbose_name="Dimension",
            ),
        ),
    ]
