# Generated by Django 4.1.2 on 2023-03-21 05:38

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_unittrustinvestment_securitiesinvestment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='epf',
            options={'verbose_name_plural': 'EPF'},
        ),
        migrations.AlterModelOptions(
            name='otherliability',
            options={'verbose_name_plural': 'Other Liabilities'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name_plural': 'Properties'},
        ),
        migrations.AlterModelOptions(
            name='socso',
            options={'verbose_name_plural': 'Socso'},
        ),
        migrations.AlterField(
            model_name='bank',
            name='account_value',
            field=django_cryptography.fields.encrypt(models.FloatField(blank=True, max_length=128, null=True)),
        ),
        migrations.AlterField(
            model_name='epf',
            name='account_value',
            field=django_cryptography.fields.encrypt(models.FloatField(blank=True, max_length=128, null=True)),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='insurance_type',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='insurance',
            name='policy_no',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='insurance',
            name='provider',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='insurance',
            name='sum_insured',
            field=django_cryptography.fields.encrypt(models.FloatField(blank=True, max_length=128, null=True)),
        ),
        migrations.AlterField(
            model_name='investment',
            name='account_value',
            field=django_cryptography.fields.encrypt(models.FloatField(blank=True, max_length=128, null=True)),
        ),
    ]