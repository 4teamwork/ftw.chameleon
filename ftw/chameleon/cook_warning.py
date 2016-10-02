from ftw.chameleon import config
from ftw.chameleon.exceptions import TemplateCookedUnexpectedly
import logging


LOG = logging.getLogger('ftw.chameleon')


def template_compiled(event):
    if not config.EAGER_PARSING:
        # The warning makes only sense when eager parsing is enabled.
        return

    if config.AUTO_RELOAD:
        # The warning makes only sense when auto reload is disabled.
        return

    msg = ('Template {!r} was unexpectedly cooked'
           ' while eager loading is enabled.'.format(event.template_path))

    if config.RECOOK_WARNING:
        LOG.warning(msg)

    if config.RECOOK_EXCEPTION:
        try:
            raise TemplateCookedUnexpectedly(msg, event.template_path)
        except TemplateCookedUnexpectedly, exc:
            LOG.exception(exc)
