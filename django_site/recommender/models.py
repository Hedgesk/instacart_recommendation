from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import pandas as pd

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 200)
    department = models.CharField(max_length = 200)
    aisle = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Ordered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])


products_df = pd.read_csv("../data/products.csv")
#departments_df = pd.read_csv("../data/departments.csv")
#aisles_df = pd.read_csv("../data/aisles.csv")


for idx, row in products_df.iterrows():
    _, created = Product.objects.get_or_create(
        name=row.product_name,
        department=row.department_id,#departments_df.loc[departments_df.department_id==row.department_id].department.values[0],
        aisle=row.aisle_id#aisles_df.loc[aisles_df.aisle_id==row.aisle_id].aisle.values[0]
    )