import pandas as pd

from scraper import scrape

metadata = pd.read_csv('data/LekkeSlaap_Kruger_metadata.csv')


if __name__ == '__main__':
    scrape(metadata)
