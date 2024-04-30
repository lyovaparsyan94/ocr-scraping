import logging.config

import yaml
from config import configs

with open(configs.DIR_CONFIG.LOG_CONFIG_FILE) as file:
    config = yaml.safe_load(file.read())
    config['handlers']['file']['filename'] = configs.DIR_CONFIG.LOG_FILE
with open(configs.DIR_CONFIG.LOG_CONFIG_FILE, 'w') as config_file:
    yaml.dump(config, config_file)


logging.config.dictConfig(config)

logger = logging.getLogger('root')
