from zope.interface import Interface


class ICompilingTemplateEvent(Interface):
    """Event triggered when chameleon compiles a template.
    """
