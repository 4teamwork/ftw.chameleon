from ftw.chameleon.events import CompilingTemplateEvent
from zope.event import notify


def chameleon_BaseTemplate_compile(self, *args, **kwargs):
    notify(CompilingTemplateEvent(self))
    return self._old__compile(*args, **kwargs)
