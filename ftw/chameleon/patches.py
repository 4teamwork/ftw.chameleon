from ftw.chameleon import config
from ftw.chameleon.events import CompilingTemplateEvent
from zope.event import notify


def chameleon_BaseTemplate_compile(self, *args, **kwargs):
    notify(CompilingTemplateEvent(self))
    return self._old__compile(*args, **kwargs)


def zope_PageTemplateFile_cook_check(self, *args, **kwargs):
    if not config.AUTO_RELOAD and self._v_program is not None:
        return
    else:
        return self._old__cook_check(*args, **kwargs)
