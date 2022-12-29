# Generated by Django 4.1.3 on 2022-12-21 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0012_reservation_roomstatus_alter_reservation_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='discount',
            field=models.CharField(blank=True, choices=[(None, 'No Discount'), ('10', '10%'), ('20', '20%'), ('30', '30%'), ('Oth', 'Other')], default='20', max_length=20, null=True),
        ),
    ]
