from ftw.chameleon import config
from ftw.chameleon import precook
from ftw.chameleon.exceptions import TemplateCookedUnexpectedly
from zope.component.hooks import getSite
import logging


LOG = logging.getLogger('ftw.chameleon')


def template_compiled(event):
    if not config.EAGER_PARSING:
        # The warning makes only sense when eager parsing is enabled.
        return

    if config.AUTO_RELOAD:
        # The warning makes only sense when auto reload is disabled.
        return

    if precook.CURRENTLY_PRECOOKING:
        # Do not spam the log when preecoking voluntarily.
        return

    site = getSite()
    site_path = site and '/'.join(site.getPhysicalPath())
    if site_path and site_path not in precook.SKINS_PRECOOKED_FOR_SITES:
        # portal_skins is not yet eager-loaded for the current site.
        # This will probably happen shortly and we keep quiet until
        # it is loaded.
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
