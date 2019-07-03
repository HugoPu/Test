import os
import logging
import time


def create_logger(model_dir):
    logger = logging.getLogger('tensorflow')
    logger.setLevel(logging.INFO)

    timestamp = str(int(time.time()))
    fh = logging.FileHandler(os.path.join(model_dir, 'log_{}.txt'.format(timestamp)))
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] ## %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)