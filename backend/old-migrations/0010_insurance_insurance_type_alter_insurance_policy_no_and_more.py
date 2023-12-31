# Generated by Django 4.1.2 on 2023-01-18 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_remove_item_encrypted_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='insurance_type',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='policy_no',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='provider',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
