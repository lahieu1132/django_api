# Generated by Django 4.0.4 on 2022-05-18 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_cart_id_remove_cartitem_id_alter_cart_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='cart_item', serialize=False, to='api.cart'),
        ),
    ]
