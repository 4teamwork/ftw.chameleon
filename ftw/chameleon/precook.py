from ftw.chameleon import config
from ftw.chameleon.progresslogger import ProgressLogger
from ftw.chameleon.utils import get_subclasses
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.pagetemplate.pagetemplate import PageTemplate
import gc
import logging
import pkg_resources
import threading


try:
    pkg_resources.get_distribution('z3c.jbot')
except pkg_resources.DistributionNotFound:
    HAS_Z3C_JBOT = False
else:
    HAS_Z3C_JBOT = True
    import z3c.jbot.patches


LOG = logging.getLogger('ftw.ptcache')
CURRENTLY_PRECOOKING = {}
SKINS_PRECOOKED_FOR_SITES = []


def eager_load_on_startup(event):
    if config.EAGER_PARSING:
        threading.Thread(target=precook_templates).start()


def precook_templates():
    CURRENTLY_PRECOOKING['precook_templates'] = True
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
        CURRENTLY_PRECOOKING.pop('precook_templates', None)


def eager_load_portal_skins(event):
    if not config.EAGER_PARSING:
        return

    for site in filter(IPloneSiteRoot.providedBy, event.request.PARENTS):
        site_path = '/'.join(site.getPhysicalPath())
        if site_path in SKINS_PRECOOKED_FOR_SITES:
            continue

        SKINS_PRECOOKED_FOR_SITES.append(site_path)
        precooking_key = 'portal_skins:{}'.format(site_path)
        CURRENTLY_PRECOOKING[precooking_key] = True
        try:
            eager_load_portal_skins_in_site(site)
        finally:
            CURRENTLY_PRECOOKING.pop(precooking_key, None)


def eager_load_portal_skins_in_site(site):
    templates = tuple(find_skins_templates(site.portal_skins))
    msg = 'Pre-cooking portal_skins: {} templates.'.format(len(templates))

    if HAS_Z3C_JBOT:
        templates += tuple(z3c.jbot.patches.registry.values())

    for template in ProgressLogger(msg, templates, logger=LOG):
        if not hasattr(template, '_cook_check'):
            continue

        try:
            template._cook_check()
        except Exception, exc:
            LOG.exception(exc)


def find_skins_templates(obj):
    if hasattr(obj, '_cook_check'):
        yield obj

    if not hasattr(obj, 'objectValues'):
        return

    for child in obj.objectValues():
        for template in find_skins_templates(child):
            yield template
