# orders/migrations/0002_add_fields_to_order.py
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),  # или какая у тебя последняя миграция
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default='', max_length=50, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default='', max_length=50, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='example@mail.com', max_length=254),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
    ]