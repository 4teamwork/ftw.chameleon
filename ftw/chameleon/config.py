from chameleon.config import AUTO_RELOAD
from chameleon.config import EAGER_PARSING
from chameleon.config import TRUE
import os


AUTO_RELOAD
EAGER_PARSING
RECOOK_WARNING = os.environ.get('FTW_CHAMELEON_RECOOK_WARNING',
                                'false').lower() in TRUE
RECOOK_EXCEPTION = os.environ.pop('FTW_CHAMELEON_RECOOK_EXCEPTION',
                                  'false').lower() in TRUE
