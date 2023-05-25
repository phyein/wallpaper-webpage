'''
Get screenshots of available webpages every 10 minutes.
Setup desktop background for a dynamically changing dashboard.
Additional settings changes required. See README.
'''

import logging as log
import logging.config
import os
import schedule
from selenium import webdriver
from selenium.webdriver.firefox import options, service
from shutil import rmtree
import time
import tomllib as toml


def load_config() -> tuple:
    '''Load configurations.'''

    with open('config_log.toml', mode='rb') as file:
        log_conf = toml.load(file)

    logging.config.dictConfig(log_conf)

    with open('config.toml', mode='rb') as file:
        conf = toml.load(file)

    # Unpack configurations. Generate destination path and file names.
    root, out, pages = conf['root'], conf['output'], conf['pages']
    if out == '': out = f'{root}\\out'
    areas, links = list(pages.keys()), list(pages.values())
    paths = [f'{out}\\{area}' for area in areas]
    all_path = f'{out}\\all'

    # determine gecko browser engine location
    loc_rel_gecko = conf['gecko_rel_path']
    loc_gecko = f'{root}\\{loc_rel_gecko}'

    return areas, links, paths, all_path, loc_gecko

def mkdir(path: str) -> None:
    '''Create directory if not exists.'''

    if not os.path.exists(path):
        os.makedirs(path)
        log.info(f'Path created: {path}')

def get_screenshots() -> None:
    '''Get screenshots using selenium webdriver.'''

    # re-load config files to adapt to changes
    areas, links, paths, all_path, loc_gecko = load_config()
    if os.path.exists(all_path): rmtree(all_path)
    mkdir(all_path)

    # setup options
    opts = options.Options()
    opts.headless = True

    # setup service
    # log_path='nul' disables geckodriver logging (it becomes too big)
    serv = service.Service(loc_gecko, log_path='nul')

    # get screenshots using selenium webdriver
    with webdriver.Firefox(options=opts, service=serv) as driver:
        for i in range(len(areas)):

            # get relevant data, ensure destination exists
            area, link, path = areas[i], links[i], paths[i]
            mkdir(path)

            try:
                driver.get(link)
                log.info(f'Success fetch: {area}')
            except:
                log.error(f'Failed fetch: {area}')

            try:
                # two images needed to make slideshow background switch
                driver.save_screenshot(f'{path}\\{area}.png')
                driver.save_screenshot(f'{path}\\{area}_1.png')
                driver.save_screenshot(f'{all_path}\\{area}.png')
                log.info(f'Success save: {area}')
            except:
                log.error(f'Failed save: {area}')

def run_schedule() -> None:
    '''Main func. Execute for direct module call but not import.'''

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

if __name__ == '__main__': run_schedule()
