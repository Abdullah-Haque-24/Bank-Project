# Generated by Django 5.0.6 on 2024-08-03 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transaction_transaction_type_transfermodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfermodel',
            old_name='reciver',
            new_name='receiver',
        ),
    ]
