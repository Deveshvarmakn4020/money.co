# Generated by Django 5.1.4 on 2025-02-23 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moneyapp", "0003_alter_member_max_eligibity_alter_member_mob"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="max_eligibity",
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name="member",
            name="mob",
            field=models.BigIntegerField(),
        ),
    ]
