import subprocess
import argparse
import logging
import logging.config

from settings import log_config

logging.config.dictConfig(log_config)
logger = logging.getLogger(__file__)


def parse_args(app_name) -> argparse.Namespace:
    parser = argparse.ArgumentParser(app_name)
    parser.add_argument("--env_file", default=".env")

    return parser.parse_args()


def main():
    args = parse_args(__file__)

    command = "airflow trigger_dag test_project"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output, error)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)
