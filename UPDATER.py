'''
Get screenshots of available webpages every 10 minutes.
Setup desktop background for a dynamically changing dashboard.
Additional settings changes required. See README.
'''

import logging as log
import logging.config
from pathlib import Path
import schedule
from selenium import webdriver
from selenium.webdriver.firefox import options, service
from shutil import rmtree
import time
import tomllib as toml


def main() -> None:

    # Run on start
    get_screenshots()

    # queue jobs in scheduler every 10 minutes
    for i in range(6):
        # schedule during N2nd minute to give webpage time to update on the N0th
        minute = f'{i}2:00'
        schedule.every().hour.at(minute).do(get_screenshots)

    # run scheduled tasks indefinitely
    while True:
        schedule.run_pending()
        time.sleep(16)

def load_config() -> tuple:
    '''Load configurations.'''

    with open('config_log.toml', mode='rb') as file:
        log_conf = toml.load(file)
    logging.config.dictConfig(log_conf)

    with open('config.toml', mode='rb') as file:
        conf = toml.load(file)

    gecko_rel_path, out, pages = conf.values()
    if out == '': out = Path('out')
    areas, links = list(pages.keys()), list(pages.values())
    paths = [Path(out, area) for area in areas]
    all_path = Path(out, 'all')
    loc_gecko = Path(loc_rel_gecko)

    return out, areas, links, paths, all_path, loc_gecko

def get_screenshots() -> None:
    '''Get screenshots using selenium webdriver.'''

    # re-load config files to adapt to changes
    out, areas, links, paths, all_path, loc_gecko = load_config()
    while not out.exists(): time.sleep(59)
    if all_path.exists(): rmtree(all_path)
    all_path.mkdir(parentns=True, exist_ok=True)

    opts = options.Options()
    opts.add_argument("--headless")
    # log_path='nul' disables geckodriver logging (it becomes too big)
    serv = service.Service(loc_gecko, log_path='nul')

    # get screenshots using selenium webdriver
    with webdriver.Firefox(options=opts, service=serv) as driver:
        for i in range(len(areas)):

            # get relevant data, ensure destination exists
            area, link, path = areas[i], links[i], paths[i]
            Path(path).mkdir(parents=True, exist_ok=True)

            try:
                driver.get(link)
                log.info(f'Success fetch: {area}')
            except:
                log.error(f'Failed fetch: {area}')

            try:
                # two images needed to make slideshow background switch
                driver.save_screenshot(Path(path, f'{area}.png'))
                driver.save_screenshot(Path(path, f'{area}_1.png'))
                driver.save_screenshot(Path(all_path, f'{area}.png'))
                log.info(f'Success save: {area}')
            except:
                log.error(f'Failed save: {area}')


if __name__ == '__main__': run_schedule()
