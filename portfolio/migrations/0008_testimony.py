# Generated by Django 3.2.6 on 2024-04-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_sitesettings_link_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=400, verbose_name='Текст')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Высказывание',
                'verbose_name_plural': 'Высказывания',
            },
        ),
    ]
