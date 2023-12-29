from django.core.management.base import BaseCommand
from faker import Faker

from shop.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(25):
            product_title = fake.company()
            product_description = fake.paragraph(nb_sentences=3)
            product_brand = fake.company()
            product_price = fake.pydecimal(left_digits=3, right_digits=2, min_value=0, max_value=999.99)
            product = Product.objects.create(
                category=Category.objects.first(),
                title=product_title,
                description=product_description,
                brand=product_brand,
                price=product_price,
                available=True,
                slug=fake.slug(),
                updated_at=fake.date_time(),
                created_at=fake.date_time(),
                discount=fake.pyint(min_value=0, max_value=50),
            )
            product.save()
        self.stdout.write(f'Successfully created, products in DB: {Product.objects.count()}!')
