# Generated by Django 4.0.2 on 2022-02-13 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_lastparsed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lastparsed',
            options={'verbose_name': 'Последний парсинг'},
        ),
        migrations.AlterModelOptions(
            name='regionalrestrictions',
            options={'ordering': ['-date', 'region'], 'verbose_name': 'Региональное ограничение', 'verbose_name_plural': 'Региональные ограничения'},
        ),
        migrations.AlterModelOptions(
            name='regionalstats',
            options={'ordering': ['-date', 'region'], 'verbose_name': 'Региональная статистика', 'verbose_name_plural': 'Региональная статистика'},
        ),
        migrations.AlterModelOptions(
            name='regions',
            options={'verbose_name': 'Регион', 'verbose_name_plural': 'Регионы'},
        ),
        migrations.AlterModelOptions(
            name='restrictions',
            options={'verbose_name': 'Ограничение', 'verbose_name_plural': 'Ограничения'},
        ),
        migrations.AlterUniqueTogether(
            name='regionalrestrictions',
            unique_together={('date', 'region')},
        ),
        migrations.AlterUniqueTogether(
            name='regionalstats',
            unique_together={('date', 'region')},
        ),
        migrations.AlterModelTable(
            name='lastparsed',
            table='last_parsed',
        ),
        migrations.AlterModelTable(
            name='regionalrestrictions',
            table='regional_restrictions',
        ),
        migrations.AlterModelTable(
            name='regionalstats',
            table='regional_stats',
        ),
        migrations.AlterModelTable(
            name='regions',
            table='regions',
        ),
    ]
