# Generated by Django 3.0.4 on 2020-03-14 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReconProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('recon_nf_file', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='study',
            name='recon_protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.ReconProtocol'),
        ),
    ]
