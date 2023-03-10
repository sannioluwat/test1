# Generated by Django 4.1.3 on 2022-12-13 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_room_roomtype'),
        ('reservations', '0006_alter_reservation_check_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='roomNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='rooms.room'),
        ),
    ]
