# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '学習してpickleで保存します'

    def add_arguments(self, parser):
        parser.add_argument('-n', default=1, type=int, help='the number of scraping pages of each category')
        
    def handle(self, *args, **options):
        page_num = options['n']
        self.stdout.write(str(page_num), ending='\n')
        
