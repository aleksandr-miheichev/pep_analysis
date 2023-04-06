import csv
from collections import defaultdict
from datetime import datetime

from .settings import BASE_DIR

STATUS_SUMMARY = 'status_summary_{current_time}.csv'
RESULTS = 'results'
STATUS_ATTRIBUTE = 'status'
DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
STATUS = 'Статус'
QUANTITY = 'Количество'
TOTAL = 'Всего'


class PepParsePipeline:
    """
    Класс Scrapy Pipeline, который обрабатывает элементы PEP, подсчитывает
    количество PEP с различными статусами, и сохраняет результаты в файл .csv
    в директории `results`.
    """
    def __init__(self):
        self.results = None
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        """
        Инициализирует счетчик статусов PEP в начале каждого запуска паука.

        Аргументы:
            - spider: паук, который начинает свой запуск.
        """
        self.results = defaultdict(int)

    def process_item(self, item, spider):
        """
        Обрабатывает элемент PEP, увеличивает счетчик для статуса PEP.

        Аргументы:
            - item: элемент PEP для обработки.
            - spider: паук, сгенерировавший элемент.
        Возвращает:
            - Обработанный элемент.
        """
        self.results[item[STATUS_ATTRIBUTE]] += 1
        return item

    def close_spider(self, spider):
        """
        Вызывается, когда паук завершает обработку. Сохраняет сводку состояния
        в файл .csv в каталоге `results`.

        Аргументы:
            - spider: паук, который закончил обработку.
        """
        file_name = self.results_dir / STATUS_SUMMARY.format(
            current_time=datetime.now().strftime(DATE_FORMAT)
        )
        with open(file_name, mode='w', encoding='utf-8', newline='') as f:
            csv.writer(f).writerows([
                (STATUS, QUANTITY),
                *self.results.items(),
                (TOTAL, sum(self.results.values()))
            ])
