from django.db import models


# Create your models here.
class Product(models.Model):
    product_title = models.CharField(
        verbose_name="Product Name",
        max_length=150
    )

    product_price = models.FloatField(
        verbose_name="Price"
    )

    product_category = models.CharField(
        verbose_name="Category",
        max_length=150
    )

    product_brand = models.CharField(
        verbose_name="Brand",
        max_length=150
    )

    def get_title(self):
        return self.product_title

    def get_price(self):
        return self.product_price

    def get_category(self):
        return self.product_category

    def get_brand(self):
        return self.product_brand

    def print_product(self):
        print("\nTitle: " + self.product_title +
              " (" + self.product_price + ")"
              )

        print("Category: " + self.product_category)
        print("Brand: " + self.product_brand)

    def store_product(self, art):
        product_info = art['data-addtional-info'].split("\"")

        self.product_title = art['data-title']
        self.product_price = product_info[3]
        self.product_category = product_info[7]
        self.product_brand = product_info[11]

        self.save(self)
