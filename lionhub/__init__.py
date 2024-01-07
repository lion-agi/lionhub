import logging
from .version import __version__

from dotenv import load_dotenv
load_dotenv()

from .utils import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)