import pandas as pd
from time import sleep
from config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC


class EndataCrawler:
    URL: str = 'https://www.endata.com.cn/BoxOffice/BO/Year/index.html'

    class Description:
        start_year: int
        end_year: int
        sleep_time: float = 1

    def __init__(self):
        self.driver, self.waiter = Config.get_resolver()
        self.driver.get(self.URL)
        self.selector = Select(self.waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#OptionDate'))))

    def __del__(self):
        self.driver.quit()

    def get_data(self, desc: Description) -> list:
        data = []
        start = desc.start_year
        while start <= desc.end_year:
            self.selector.select_by_visible_text(f"{start}年")
            sleep(desc.sleep_time)
            movie_data = self.driver.find_element(By.CSS_SELECTOR, '#TableList > table')
            line_elements = movie_data.text.split('\n')
            row = 2
            while row < len(line_elements):
                tmp_list = [f"{start}年", line_elements[row]]
                for e in line_elements[row + 1].split(' '):
                    tmp_list.append(e)
                data.append(tmp_list)
                row = row + 3
            start = start + 1
        return data

    @staticmethod
    def gen_dataframe(data: list[str]) -> pd.DataFrame:
        return pd.DataFrame(data, columns=[
            '年份',
            '影片',
            '类型',
            '总票房（万）',
            '平均票价',
            '场均人次',
            '国家及地区',
            '上映日期'
        ])
