# Generated by Django 4.1.4 on 2022-12-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(max_length=1000),
        ),
    ]
