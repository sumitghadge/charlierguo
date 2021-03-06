# Generated by Django 4.0.3 on 2022-03-22 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("street1", models.CharField(max_length=1024)),
                ("street2", models.CharField(max_length=1024)),
                ("city", models.CharField(max_length=1024)),
                ("state", models.CharField(max_length=1024)),
                ("zipcode", models.CharField(max_length=1024)),
                ("country_name", models.CharField(max_length=1024)),
                ("country_code", models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=1024)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("active", "Active")],
                        max_length=1024,
                    ),
                ),
                ("price", models.FloatField()),
                ("vendor", models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1024)),
                ("email", models.CharField(max_length=1024)),
                ("subtotal", models.FloatField()),
                ("taxes", models.FloatField()),
                ("shipping", models.FloatField()),
                ("total", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("shipped_at", models.DateTimeField(blank=True, null=True)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="crowdmadeapp.address",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("total", models.FloatField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="crowdmadeapp.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="crowdmadeapp.product",
                    ),
                ),
            ],
        ),
    ]
