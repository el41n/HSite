# Generated by Django 2.0.4 on 2018-05-17 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_memory_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='motherboard',
            name='form_factor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.FormFactor'),
        ),
        migrations.AlterField(
            model_name='hardware',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hardware', to='catalog.Vendor'),
        ),
    ]