import csv
from collections import defaultdict
from datetime import datetime

from scrapy.exceptions import DropItem

from .settings import BASE_DIR

NO_STATUS = 'Статус не найден!'
STATUS_SUMMARY = 'status_summary_{current_time}.csv'
RESULTS = 'results'
STATUS_ATTRIBUTE = 'status'
DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
ENCODING_FORMAT = 'utf-8'
STATUS = 'Статус'
QUANTITY = 'Количество'
TOTAL = 'Total'
FILE_OPEN_MODE = 'w'


class PepParsePipeline:
    """
    Класс Scrapy Pipeline, который обрабатывает элементы PEP, подсчитывает
    количество PEP с различными статусами, и сохраняет результаты в файл .csv
    в директории `results`.
    """
    def __init__(self):
        self.results = defaultdict(int)
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        """
        Обрабатывает элемент PEP, увеличивает счетчик для статуса PEP.

        Аргументы:
            - item: элемент PEP для обработки.
            - spider: паук, сгенерировавший элемент.
        Возвращает:
            - Обработанный элемент.
        """
        if STATUS_ATTRIBUTE not in item:
            raise DropItem(NO_STATUS)
        self.results[item[STATUS_ATTRIBUTE]] += 1
        return item

    def close_spider(self, spider):
        """
        Вызывается, когда паук завершает обработку. Сохраняет сводку состояния
        в файл .csv в каталоге `results`.

        Аргументы:
            - spider: Паук, который закончил обработку.
        """
        file_name = self.results_dir / STATUS_SUMMARY.format(
            current_time=datetime.now().strftime(DATE_FORMAT)
        )
        with open(
                file_name,
                mode=FILE_OPEN_MODE,
                encoding=ENCODING_FORMAT,
                newline=''
        ) as f:
            writer = csv.DictWriter(f, fieldnames=[STATUS, QUANTITY])
            writer.writeheader()
            for status, quantity in self.results.items():
                writer.writerow({STATUS: status, QUANTITY: quantity})
            writer.writerow(
                {STATUS: TOTAL, QUANTITY: sum(self.results.values())}
            )
