from django.core.management.base import BaseCommand
from products.dbbuilder import select_products


class Command(BaseCommand):
    help = "populatedb from API OFF"

    def handle(self, *args, **kwargs):
        select_products()
        #selector = ProductSelector()
        #selector.select_products()

