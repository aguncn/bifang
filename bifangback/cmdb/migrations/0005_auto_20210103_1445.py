# Generated by Django 3.1.4 on 2021-01-03 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0004_action_historicalaction_historicalpermission_permission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'verbose_name': 'Action权限', 'verbose_name_plural': 'Action权限'},
        ),
        migrations.AlterModelOptions(
            name='historicalaction',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Action权限'},
        ),
        migrations.AlterModelOptions(
            name='historicalpermission',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Permission应用权限'},
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'verbose_name': 'Permission应用权限', 'verbose_name_plural': 'Permission应用权限'},
        ),
        migrations.AlterModelTable(
            name='action',
            table='Action',
        ),
        migrations.AlterModelTable(
            name='permission',
            table='Permission',
        ),
    ]
