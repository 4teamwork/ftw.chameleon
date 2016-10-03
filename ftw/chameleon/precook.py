from ftw.chameleon import config
from ftw.chameleon.progresslogger import ProgressLogger
from ftw.chameleon.utils import get_subclasses
from zope.pagetemplate.pagetemplate import PageTemplate
import gc
import logging
import threading


LOG = logging.getLogger('ftw.ptcache')
CURRENTLY_PRECOOKING = False


def eager_load_on_startup(event):
    if config.EAGER_PARSING:
        threading.Thread(target=precook_templates).start()


def precook_templates():
    globals()['CURRENTLY_PRECOOKING'] = True
    try:
        ptclasses = tuple(get_subclasses(PageTemplate))
        templates = filter(lambda obj: isinstance(obj, ptclasses),
                           gc.get_referrers(*ptclasses))

        msg = 'Pre-cooking {} templates.'.format(len(templates))
        for template in ProgressLogger(msg, templates, logger=LOG):
            if not hasattr(template, '_cook_check'):
                continue

            try:
                template._cook_check()
            except Exception, exc:
                LOG.exception(exc)

    finally:
        globals()['CURRENTLY_PRECOOKING'] = False
