import os
import time
import argparse
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# parser = argparse.ArgumentParser()
# parser.add_argument("--year", type=int, default="2023", help="Year of OpenReview papers. (default: 2023)")
# parser.add_argument('--pages', type=int, default=100, help='Number of pages on the website. (default: 100)')
# args = parser.parse_args()

class Base:
    def __init__(self, url='', sep='|', is_headless=False, params={}):
        self.url = url
        self.sep = sep
        self.is_headless = is_headless
        self.params = params

    def _create_driver(self):
        # driver = webdriver.Edge('msedgedriver.exe')
        if self.is_headless:
            # https://stackoverflow.com/questions/53657215/running-selenium-with-headless-chrome-webdriver
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            # chrome_options.add_argument("--disable-extensions")
            # chrome_options.add_argument("--disable-gpu")
            # chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
            # chrome_options.headless = True # also works
            options = chrome_options
        else:
            options = None

        # download from https://sites.google.com/chromium.org/driver/
        driver = webdriver.Chrome('./chromedriver', options=options)
        # driver.get(f'https://openreview.net/group?id=ICLR.cc/{args.year}/Conference')
        driver.get(self.url)
        # print(driver.page_source.encode("utf-8"))

        # mimic human operations to avoid access failure, which is very important.
        paper_type = self.params['paper_type']
        # cond = EC.presence_of_element_located((By.XPATH, f"//*/div[@id='{paper_type}']/ul/li/a"))
        # WebDriverWait(driver, 3).until(cond)  # wait 3 seconds on the current website.

        return driver

    def _obtain_out_file(self):
        out_dir = self.params['out_dir']
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_csv = os.path.join(out_dir, '_'.join([self.params['name'], str(self.params['year']),
                                              self.params['paper_type']]) + '.csv')
        return out_csv

    def parsing_url(self):
        pass


class ICRL(Base):

    def __init__(self, url='', sep='|', is_headless=True, params={}):
        #super.__init__()
        self.url = url
        self.sep = sep
        self.is_headless = is_headless
        self.params = params

    def parsing_url(self):

        driver = self._create_driver()

        self.out_csv = self._obtain_out_file()
        with open(self.out_csv, 'w', encoding='utf8') as f:
            f.write(f'{self.sep}'.join(['paper_id', 'title', 'link', 'keywords', 'abstract']) + '\n')
            paper_type = self.params['paper_type']
            for page in tqdm(range(0, 100), initial=1):
                print(f'Parsing the {page + 1}th page...')
                texts = ''
                # https://stackoverflow.com/questions/35606708/what-is-the-difference-between-and-in-xpath
                # Square brackets mean the condition for any nodes:
                #      Starting from the root node (//),  find any "div" nodes which have "id='notable-top-5-'"
                elems = driver.find_elements(by=By.XPATH, value=f"//*/div[@id='{paper_type}']/ul/li")
                for i, elem in enumerate(elems):
                    try:
                        # parse title
                        # print(i, elem.text, flush=True)
                        # if elem.text !='Notable-top-5%': continue
                        title = elem.find_element(by=By.XPATH, value='./h4/a[1]')
                        link = title.get_attribute('href')
                        paper_id = link.split('=')[-1]
                        title = title.text.strip().replace('\t', ' ').replace('\n', ' ')
                        # show details
                        elem.find_element(by=By.XPATH, value='./a').click()
                        time.sleep(0.2)
                        # parse keywords & abstract
                        items = elem.find_elements(by=By.XPATH, value='.//li')
                        keyword = ''.join([x.text for x in items if 'Keywords' in x.text])
                        abstract = ''.join([x.text for x in items if 'Abstract' in x.text])
                        keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ').replace('Keywords: ', '')
                        abstract = abstract.strip().replace('\t', ' ').replace('\n', ' ').replace('Abstract: ', '')
                        texts += f'{self.sep}'.join([paper_id, title, link, keyword, abstract]) + '\n'
                        # print(i, elem.text, flush=True)
                    except Exception as e:
                        # print(f'page {page}, # {i}:', e)
                        continue

                print(f'page={page + 1}, texts: {texts}', flush=True)
                f.write(texts)
                f.flush()

                # next page
                try:
                    # https://www.lambdatest.com/blog/complete-guide-for-using-xpath-in-selenium-with-examples/
                    # //: denotes the current node
                    # print(driver.find_element(by=By.XPATH, value='//*["all-submissions"]/nav/ul/li/a').text, flush=True)
                    # driver.find_element(by=By.XPATH,
                    #                     value=f"//*/div[@id='notable-top-5-']/nav/ul/li[@data-page-number='{page + 1}']/a").click()
                    driver.find_element(by=By.XPATH,
                                        value=f"//*/div[@id='{paper_type}']/nav/ul/li[@data-page-number='{page + 1}']/a").click()
                    time.sleep(3)  # NOTE: increase sleep time in seconds if needed //*[@id="notable-top-5-"]
                except Exception as e:
                    print(e)
                    # print('no next page, exit.')
                    break
        driver.quit()

        return self.out_csv


class NeurIPS(Base):

    def __init__(self, url='', sep='|', is_headless=False, params={}):
        #super.__init__()
        self.url = url
        self.sep = sep
        self.is_headless = is_headless
        self.params = params

    def parsing_url(self):

        driver = self._create_driver()

        self.out_csv = self._obtain_out_file()
        with open(self.out_csv, 'w', encoding='utf8') as f:
            f.write(f'{self.sep}'.join(['paper_id', 'title', 'link', 'keywords', 'abstract']) + '\n')
            paper_type = self.params['paper_type']
            for page in tqdm(range(0, 100), initial=1):
                print(f'Parsing the {page + 1}th page...')
                texts = ''
                # https://stackoverflow.com/questions/35606708/what-is-the-difference-between-and-in-xpath
                # Square brackets mean the condition for any nodes:
                #      Starting from the root node (//),  find any "div" nodes which have "id='notable-top-5-'"
                # https://openreview.net/group?id=NeurIPS.cc/2022/Conference
                elems = driver.find_elements(by=By.XPATH, value=f"//*/div[@id='{paper_type}']/ul/li")
                for i, elem in enumerate(elems):
                    try:
                        # parse title
                        # print(i, elem.text, flush=True)
                        # if elem.text !='Notable-top-5%': continue
                        title = elem.find_element(by=By.XPATH, value='./h4/a[1]')
                        link = title.get_attribute('href')
                        paper_id = link.split('=')[-1]
                        title = title.text.strip().replace('\t', ' ').replace('\n', ' ')
                        # show details
                        elem.find_element(by=By.XPATH, value='./a').click()
                        time.sleep(0.2)
                        # parse keywords & abstract
                        items = elem.find_elements(by=By.XPATH, value='.//li')
                        keyword = ''.join([x.text for x in items if 'Keywords' in x.text])
                        abstract = ''.join([x.text for x in items if 'Abstract' in x.text])
                        keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ').replace('Keywords: ', '')
                        abstract = abstract.strip().replace('\t', ' ').replace('\n', ' ').replace('Abstract: ', '')
                        texts += f'{self.sep}'.join([paper_id, title, link, keyword, abstract]) + '\n'
                        # print(i, elem.text, flush=True)
                    except Exception as e:
                        # print(f'page {page}, # {i}:', e)
                        continue

                print(f'page={page + 1}, texts: {texts}', flush=True)
                f.write(texts)
                f.flush()

                # next page
                try:
                    # https://www.lambdatest.com/blog/complete-guide-for-using-xpath-in-selenium-with-examples/
                    # //: denotes the current node
                    # print(driver.find_element(by=By.XPATH, value='//*["all-submissions"]/nav/ul/li/a').text, flush=True)
                    driver.find_element(by=By.XPATH,
                                        value=f"//*/div[@id='{paper_type}']/nav/ul/li[@data-page-number='{page + 1}']/a").click()
                    time.sleep(3)  # NOTE: increase sleep time in seconds if needed
                except Exception as e:
                    print(e)
                    # print('no next page, exit.')
                    break
        driver.quit()

        return self.out_csv



class ICML(Base):

    def __init__(self, url='', sep='|', is_headless=False, params={}):
        # super.__init__()
        self.url = url
        self.sep = sep
        self.is_headless = is_headless
        self.params = params

    def parsing_url(self):

        driver = self._create_driver()

        self.out_csv = self._obtain_out_file()
        with open(self.out_csv, 'w', encoding='utf8') as f:
            f.write(f'{self.sep}'.join(['paper_id', 'title', 'link', 'keywords', 'abstract']) + '\n')
            paper_type = self.params['paper_type']
            for page in tqdm(range(0, 100), initial=1):
                print(f'Parsing the {page + 1}th page...')
                texts = ''
                # https://stackoverflow.com/questions/35606708/what-is-the-difference-between-and-in-xpath
                # Square brackets mean the condition for any nodes:
                #      Starting from the root node (//),  find any "div" nodes which have "id='notable-top-5-'"
                # 'https://icml.cc/virtual/2022/events/spotlight' <div class="grid-displaycards">
                elems = driver.find_elements(by=By.XPATH, value=f"//*/div[@class='{paper_type}']/div[@class='displaycards touchup-date']")
                for i, elem in enumerate(elems):
                    try:
                        # parse title
                        # print(i, elem.text, flush=True)
                        # if elem.text !='Notable-top-5%': continue
                        title = elem.find_element(by=By.XPATH, value="./*/a[@class='small-title']")
                        link = title.get_attribute('href')
                        paper_id = elem.get_attribute('id')
                        title = title.text.strip().replace('\t', ' ').replace('\n', ' ')
                        # show details
                        # elem.find_element(by=By.XPATH, value="./*/a[@class='small-title']").click()
                        # time.sleep(0.2)
                        # parse keywords & abstract
                        item = elem.find_element(by=By.XPATH, value="./div/div[@class=\"abstract-display\"]")
                        # keyword = ''.join([x.text for x in items if 'Keywords' in x.text])
                        # abstract = ''.join([x.text for x in items if 'Abstract' in x.text])
                        abstract = item.text
                        # keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ').replace('Keywords: ', '')
                        keyword = ''
                        # abstract = abstract.strip().replace('\t', ' ').replace('\n', ' ').replace('Abstract: ', '')
                        texts += f'{self.sep}'.join([paper_id, title, link, keyword, abstract]) + '\n'
                        print(i, paper_id,  abstract, flush=True)
                    except Exception as e:
                        print(f'page {page}, # {i}, {elem.text}', e)
                        continue

                print(f'page={page + 1}, texts: {texts}', flush=True)
                f.write(texts)
                f.flush()

                break
                # # next page
                # try:
                #     # https://www.lambdatest.com/blog/complete-guide-for-using-xpath-in-selenium-with-examples/
                #     # //: denotes the current node
                #     # print(driver.find_element(by=By.XPATH, value='//*["all-submissions"]/nav/ul/li/a').text, flush=True)
                #     driver.find_element(by=By.XPATH,
                #                         value=f"//*/div[@class='{paper_type}']/nav/ul/li[@data-page-number='{page + 1}']/a").click()
                #     time.sleep(3)  # NOTE: increase sleep time in seconds if needed
                # except Exception as e:
                #     print(e)
                #     # print('no next page, exit.')
                #     break
        driver.quit()

        return self.out_csv
