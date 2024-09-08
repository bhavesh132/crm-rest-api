from django.core.management.base import BaseCommand
from django.db import connection
from authentication.models import * # Import all your models
from service.models import *
from customer.models import *
from sales.models import *
from django.core.management.color import no_style



class Command(BaseCommand):
    help = 'Reset the sequence for all models'

    def handle(self, *args, **kwargs):
        models = [Ticket, Note, SubType, Type, Task, NewsFeed, Contact, Company, Opportunity, Campaign]  # List all models here

        sequence_sql = connection.ops.sequence_reset_sql(no_style(), models)
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
                self.stdout.write(f'Reset sequence: {sql}')

        self.stdout.write(self.style.SUCCESS('Successfully reset sequences for all models'))