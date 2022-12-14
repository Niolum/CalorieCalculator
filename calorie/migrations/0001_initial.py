# Generated by Django 4.1.1 on 2022-09-13 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('photo', models.ImageField(upload_to='category/', verbose_name='Изображение')),
                ('slug', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('photo', models.ImageField(upload_to='product/', verbose_name='Изображение')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('calorie', models.FloatField(verbose_name='Ккал')),
                ('fat', models.FloatField(verbose_name='Жиры')),
                ('protein', models.FloatField(verbose_name='Белки')),
                ('carbohydrate', models.FloatField(verbose_name='Углеводы')),
                ('slug', models.SlugField(max_length=160, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calorie.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_calorie', models.FloatField(default=0, null=True)),
                ('total_fat', models.FloatField(default=0, null=True)),
                ('total_protein', models.FloatField(default=0, null=True)),
                ('total_carbohydrate', models.FloatField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calorie_amount', models.FloatField(blank=True, default=0, null=True)),
                ('fat_amount', models.FloatField(blank=True, default=0, null=True)),
                ('protein_amount', models.FloatField(blank=True, default=0, null=True)),
                ('carbohydrate_amount', models.FloatField(blank=True, default=0, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.product', verbose_name='Продукт')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.profile', verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='all_food_selected',
            field=models.ManyToManyField(related_name='all_product', through='calorie.ProfileFood', to='calorie.product', verbose_name='Все выбранные продукты'),
        ),
        migrations.AddField(
            model_name='profile',
            name='food_selected',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calorie.product', verbose_name='Выбранный продукт'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
