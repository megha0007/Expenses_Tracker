# Generated by Django 5.1.3 on 2025-07-29 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Transport', 'Transport'), ('Utilities', 'Utilities'), ('Entertainment', 'Entertainment'), ('Other', 'Other')], max_length=50)),
                ('date', models.DateField()),
            ],
        ),
    ]
