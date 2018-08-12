# Generated by Django 2.0.7 on 2018-08-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_ticket_feature_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='solution',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='feature_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Contribution towards feature development'),
        ),
    ]