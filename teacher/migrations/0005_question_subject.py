# Generated by Django 2.2.4 on 2019-09-03 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_auto_20190903_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='teacher.Subject'),
            preserve_default=False,
        ),
    ]