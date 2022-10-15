# Generated by Django 4.1.1 on 2022-09-21 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="item",
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
                ("item_name", models.CharField(max_length=200)),
                ("item_disc", models.CharField(max_length=200)),
                ("item_price", models.IntegerField()),
            ],
        ),
    ]
