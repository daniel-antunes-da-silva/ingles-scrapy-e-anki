# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
from .settings import XLSX_PATH
import shutil

CAMPOS = ['Frase', 'Palavra', 'Tradução']


class XLSXPipeline(object):
    planilha = None
    sheet = None

    def open_spider(self, spider):
        self.planilha = openpyxl.Workbook()
        self.sheet = self.planilha.active
        self.sheet.append(CAMPOS)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.sheet.append(['', adapter.get('Palavra'), ', '.join(adapter.get('Tradução')[:3])])

        return item

    def close_spider(self, spider):
        self.planilha.save(XLSX_PATH)

