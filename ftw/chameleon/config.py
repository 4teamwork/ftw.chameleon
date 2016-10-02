from chameleon.config import AUTO_RELOAD
from chameleon.config import EAGER_PARSING
from chameleon.config import environment
from chameleon.config import TRUE


AUTO_RELOAD
EAGER_PARSING
RECOOK_WARNING = environment.pop('recook_warning', 'false').lower() in TRUE
RECOOK_EXCEPTION = environment.pop('recook_exception', 'false').lower() in TRUE
