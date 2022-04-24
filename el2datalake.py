#!/usr/local/bin/python
import os
import sys
import yaml
import json
import logging
import requests
from datetime import datetime, timedelta
from azure.storage.filedatalake import DataLakeServiceClient

logging.basicConfig(stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

date = datetime.today() - timedelta(days=2)
previous_date = f"{date.year}-{date.month}-{date.day}"


def extract():
    logger.info('EXTRACTING...')
    #extract data from API
    url = 'https://indicadores.integrasus.saude.ce.gov.br/api/casos-coronavirus?dataInicio='+ previous_date +'&dataFim=' + previous_date
    req = requests.get(url)
    data = req.json()
    
    if data:
        with open(f'covid-data-{previous_date}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        logger.info('THERE IS NOT DATA')

def initialize_storage_account(storage_account_name, storage_account_key):
    try:
        global service_client
        service_client = DataLakeServiceClient(account_url="https://"+ storage_account_name +".dfs.core.windows.net", credential=storage_account_key)

    except Exception as e:
        logger.info('EXCEPTION...')
        logger.info(e)

def create_file_system(container_name):
    try:
        global file_system_client
        logger.info('CREATING A CONTAINER NAMED AZ-COVID-DATA')
        file_system_client = service_client.create_file_system(file_system=container_name)

    except Exception as e:
        logger.info('EXCEPTION...')
        logger.info(e)

def create_directory():
    try:
        logger.info('CREATING A DIRECTORY NAMED DIRECTORY-COVID22')
        file_system_client.create_directory("directory-covid19")

    except Exception as e:
        logger.info('EXCEPTION...')
        logger.info(e)

def upload_file_to_container_datalake(local_file, container_name):
    try:
        logger.info('UPLOADING FILE TO AZURE DATA LAKE STORAGE...')
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        directory_client = file_system_client.get_directory_client("directory-covid19")

        file_client = directory_client.get_file_client(f"covid-{previous_date}.json")

        with open(local_file, "rb") as data:
            file_client.upload_data(data, overwrite=True)
            logger.info('UPLOADED TO AZURE DATA LAKE')

    except Exception as e:
        logger.info('EXCEPTION...')
        logger.info(e)

def load_config():
    directory = os.path.dirname(os.path.abspath(__file__))
    with open(directory + "/config.yaml", "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)


if __name__ == "__main__":
    extract()
    config = load_config()
    initialize_storage_account(config["AZURE_DL_STORAGE_ACCOUNT_NAME"], config["AZURE_DL_ACCOUNT_KEY"])
    create_file_system(config["AZURE_DL_CONTAINER_NAME"])
    upload_file_to_container_datalake(f"covid-data-{previous_date}.json", config["AZURE_DL_CONTAINER_NAME"])
