import pandas as pd
from config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class MaoyanCrawler:
    URL_PREFIX: str = 'https://piaofang.maoyan.com/dashboard/movie?date='

    FONT_MAPS: dict[str, dict[str, int]] = {
        'e3dfe524': {'\ueb19': 9, '\ue3ec': 2, '\uf7d2': 4, '\ued30': 1, '\uf3e8': 5, '\uf11c': 3, '\uea60': 6, '\uef28': 8, '\uea6f': 0, '\ue3df': 7},
        '2a70c44b': {'\ue132': 7, '\ue83d': 5, '\ue583': 3, '\uec4b': 9, '\ueba2': 0, '\ue886': 2, '\uf23f': 6, '\uf16b': 4, '\ued8f': 1, '\uf05a': 8},
        '20a70494': {'\ueb92': 7, '\ue8d7': 3, '\uf7ff': 6, '\uf85e': 1, '\ue99c': 2, '\uf1fc': 8, '\uf726': 0, '\ue8ee': 4, '\ue9ea': 9, '\uecdc': 5},
        '75e5b39d': {'\uf66d': 0, '\uf615': 3, '\ue1b7': 8, '\uec68': 2, '\ue5ac': 6, '\ue317': 7, '\ue274': 9, '\ueab3': 4, '\ue6d5': 1, '\uef74': 5},
        '432017e7': {'\uf7b3': 0, '\ued98': 9, '\uf70e': 6, '\uf0f0': 2, '\ued4f': 5, '\ue85f': 3, '\ue83f': 8, '\ue916': 7, '\uedba': 1, '\uefe9': 4}
    }

    @staticmethod
    def get_font_map(key) -> dict[str, int] | None:
        for name, mapper in MaoyanCrawler.FONT_MAPS.items():
            if key in mapper:
                return mapper
        return None

    class Description:
        start_date: str
        end_date: str

    def __init__(self):
        self.driver, self.waiter = Config.get_resolver()

    def __del__(self):
        self.driver.quit()

    def get_data(self, desc: Description) -> list:
        data: list = []
        dates = pd.date_range(start=desc.start_date, end=desc.end_date, freq='D')
        for date in dates:
            date_str = date.strftime('%Y-%m-%d')
            url = self.URL_PREFIX + date_str
            self.driver.get(url)
            movie_data = self.waiter.until(EC.visibility_of_element_located((By.XPATH, "//table[@class='dashboard-table']/tbody")))

            line_elements = movie_data.text.split('\n')
            font_map = {}

            row = 1
            init_map = False
            while row < len(line_elements):
                # 1. name
                tmp_list = [date_str, line_elements[row]]
                row = row + 1

                # 2. mode + total amount
                if line_elements[row + 1].endswith('万'):
                    e2 = line_elements[row].strip().split(' ')
                    row = row + 1
                    if len(e2) == 1:
                        val = e2[0].strip()
                        if val.endswith('万') or val.endswith('亿') or val[-1].isdigit():
                            tmp_list.append('')
                            tmp_list.append(val)
                        else:
                            tmp_list.append(val)
                            tmp_list.append('')
                    else:
                        tmp_list.append(e2[0])
                        tmp_list.append(e2[-1])
                else:
                    tmp_list.append('')
                    tmp_list.append('')

                # 3. decode realtime amount
                if not init_map:
                    font_map = self.get_font_map(line_elements[row][0])
                    init_map = True

                amount = []
                for c in line_elements[row].strip():
                    if c == '.' or c == '万':
                        amount.append(c)
                    else:
                        amount.append(font_map[c])
                tmp_list.append(''.join(map(str, amount)))
                row = row + 1

                # 4. misc
                for val in line_elements[row].split(' '):
                    tmp_list.append(val)
                row = row + 2

                data.append(tmp_list)
        return data

    @staticmethod
    def gen_dataframe(data: list[str]) -> pd.DataFrame:
        return pd.DataFrame(data, columns=[
            '日期',
            '影片',
            '上映信息',
            '总票房',
            '当日综合票房',
            '票房占比',
            '排片场次',
            '排片占比',
            '场均人次',
            '上座率'
        ])
