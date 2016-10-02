from ftw.chameleon.interfaces import ICompilingTemplateEvent
from zope.interface import implements


class CompilingTemplateEvent(object):
    implements(ICompilingTemplateEvent)

    def __init__(self, template):
        self.template = template
        self.template_path = getattr(template, 'filename', None)
