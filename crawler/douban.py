import pandas as pd
from config import Config
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class DoubanCrawler:
    URL: str = 'https://movie.douban.com'

    class Description:
        filename: str

    def __init__(self):
        self.driver, self.waiter = Config.get_resolver()
        self.driver.get(self.URL)

    def __del__(self):
        self.driver.quit()

    def get_data(self, desc: Description) -> list:
        search = self.waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#inp-query')))
        search.clear()
        search.send_keys(desc.filename + Keys.ENTER)

        titles = self.waiter.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='title']")))
        if titles[0].find_element(By.XPATH, "./following-sibling::div[1]").text.endswith('人收藏'):
            titles[1].find_element(By.XPATH, "./a").click()
        else:
            titles[0].find_element(By.XPATH, "./a").click()

        infos = self.waiter.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='info']")))

        res = [''] * 15
        res[0] = desc.filename
        for info in infos.text.split('\n'):
            if info.startswith('导演'):
                res[1] = info[4:]
            elif info.startswith('编剧'):
                res[2] = info[4:]
            elif info.startswith('主演'):
                res[3] = info[4:]
            elif info.startswith('类型'):
                res[4] = info[4:]
            elif info.startswith('片长'):
                res[5] = info[4:]

        try:
            scores = self.waiter.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='interest_sectl']")))
            score_elements = scores.text.split('\n')
            if len(score_elements) > 10:
                start = 1
                if score_elements[start].find('引用') != -1:
                    start = 2
                res[6] = score_elements[start]
                res[7] = score_elements[start + 1]
                res[8] = score_elements[start + 3]
                res[9] = score_elements[start + 5]
                res[10] = score_elements[start + 7]
                res[11] = score_elements[start + 9]
                res[12] = score_elements[start + 11]
                res[13] = ','.join(score_elements[start + 12:])
        except:
            pass

        try:
            summary = self.waiter.until(EC.visibility_of_element_located((By.XPATH, "//span[@property='v:summary']")))
            res[14] = summary.text
        except:
            pass

        return res

    @staticmethod
    def gen_dataframe(data: list[str]) -> pd.DataFrame:
        return pd.DataFrame(data, columns=[
            '影片',
            '导演',
            '编剧',
            '主演',
            '类型',
            '片长',
            '综合评分',
            '评分人数',
            '5星评分占比',
            '4星评分占比',
            '3星评分占比',
            '2星评分占比',
            '1星评分占比',
            '同类比较',
            '剧情简介',
        ])
