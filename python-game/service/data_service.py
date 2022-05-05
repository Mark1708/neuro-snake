from config import RESOURCE_PATH
from datetime import datetime
import pytz

from service.report_service import ReportService

class DataService:
    def __init__(self):
        self.recourse_path = RESOURCE_PATH

        self.tz_info = pytz.timezone('Europe/Moscow')
        self.time = None
        self.last_time = None
        self.name = None
        self.file = None

        self.state = 'CREATE'  # 'WRITE' 'FINISH'

    def start_writing(self, data):
        self.time = datetime.now(self.tz_info)
        self.name = f'{self.recourse_path}data_{self.time.strftime("%d.%m.%Y_%H.%M.%S")}.csv'
        self.file = open(self.name, "a")
        self.write_data(data)
        self.state = 'WRITE'

    def write_data(self, data):
        self.last_time = datetime.now(self.tz_info)
        real_time = self.last_time.timestamp() - self.time.timestamp()
        self.file.write(f'{real_time},{data}\n')

    def finished(self, score):
        self.file.close()
        self.state = 'FINISH'

        report_service = ReportService(self, score)
        report_service.run_process()
