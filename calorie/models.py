from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from pytils.translit import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    photo = models.ImageField(verbose_name='Изображение', upload_to='category/')
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


def product_directory_path(instance, filename):
    return 'product/{0}/{1}'.format(instance.category.name, filename)


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    photo = models.ImageField(verbose_name='Изображение', upload_to=product_directory_path)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=1)
    calorie = models.FloatField(verbose_name='Ккал')
    fat = models.FloatField(verbose_name='Жиры')
    protein = models.FloatField(verbose_name='Белки')
    carbohydrate = models.FloatField(verbose_name='Углеводы')
    slug = models.SlugField(max_length=160, unique=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.PROTECT)
    description = models.TextField(verbose_name='Описание', default='')
    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.name}-{self.category.name}"

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    food_selected = models.ForeignKey(Product, verbose_name='Выбранный продукт', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    total_calorie = models.FloatField(verbose_name='Общее число каллорий', default=0,null=True)
    total_fat = models.FloatField(verbose_name='Общее число жиров', default=0,null=True)
    total_protein = models.FloatField(verbose_name='Общее число белков', default=0,null=True)
    total_carbohydrate = models.FloatField(verbose_name='Общее число углеводов', default=0,null=True)
    all_food_selected = models.ManyToManyField(Product, through='ProfileFood', verbose_name='Все выбранные продукты', related_name='all_product')

    def save(self, *args, **kwargs):
        if self.food_selected != None:
            self.total_calorie = self.food_selected.calorie * self.food_selected.quantity
            self.total_fat = self.food_selected.fat * self.food_selected.quantity
            self.total_protein = self.food_selected.protein * self.food_selected.quantity
            self.total_carbohydrate = self.food_selected.carbohydrate * self.food_selected.quantity
            profile = Profile.objects.filter(user=self.user).last()
            ProfileFood.objects.create(
                profile=profile, 
                product=self.food_selected, 
                calorie_amount=self.total_calorie,
                fat_amount=self.total_fat,
                protein_amount=self.total_protein,
                carbohydrate_amount=self.total_carbohydrate
                )
            self.food_selected = None
            super(Profile, self).save(*args, **kwargs)
        else:
            super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'




class ProfileFood(models.Model):
    profile = models.ForeignKey(Profile, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    calorie_amount = models.FloatField(default=0, null=True, blank=True)
    fat_amount = models.FloatField(default=0, null=True, blank=True)
    protein_amount = models.FloatField(default=0, null=True, blank=True)
    carbohydrate_amount = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.profile.username}"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Продукт пользователя'
        verbose_name_plural = 'Продукты пользователя'


