# Generated by Django 4.2.11 on 2024-05-01 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0002_alter_libro_options_autor_imagen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='libro',
            options={'verbose_name': 'libro', 'verbose_name_plural': 'libros'},
        ),
    ]
