# Generated by Django 4.1.3 on 2022-12-28 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_room_desc'),
        ('reservations', '0017_rename_pay_type_reservation_payment_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='credit_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='paid_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='total_cost',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment_type',
            field=models.CharField(choices=[('P', 'Paying'), ('PD', 'Paying Debtor'), ('NP', 'Non Paying')], default='NP', max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='roomNumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_reserve', to='rooms.room'),
        ),
    ]
