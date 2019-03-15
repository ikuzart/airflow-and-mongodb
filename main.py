import argparse
import logging.config

DEFAULT_CONFIG_PATH = "config.cfg"

# logging.config.dictConfig(log_config)
logger = logging.getLogger(__file__)


def parse_args(app_name) -> argparse.Namespace:
    parser = argparse.ArgumentParser(app_name)
    parser.add_argument("--config", help="config")
    return parser.parse_args()


def main():
    args = parse_args(__file__)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)
