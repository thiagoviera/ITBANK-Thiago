from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.IntegerField()),
                ('card_numero', models.TextField(unique=True)),
                ('card_expiracion_fecha', models.TextField()),
                ('card_emision_fecha', models.TextField()),
                ('card_cvv', models.CharField(max_length=200)),
                ('card_tipo', models.TextField()),
                ('customer_id', models.IntegerField()),
                ('card_brand_id', models.IntegerField()),
            ],
            options={
                'db_table': 'tarjeta',
                'managed': False,
            },
        ),
    ]
