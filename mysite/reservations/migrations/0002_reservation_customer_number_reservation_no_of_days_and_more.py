# Generated by Django 4.1.3 on 2022-11-22 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='customer_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='no_of_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='check_in',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='check_out',
            field=models.DateField(),
        ),
    ]
