from ftw.testing.layer import COMPONENT_REGISTRY_ISOLATION
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class ChameleonLayer(PloneSandboxLayer):
    defaultBases = (COMPONENT_REGISTRY_ISOLATION, )

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)


CHAMELEON_FIXTURE = ChameleonLayer()
CHAMELEON_FUNCTIONAL = FunctionalTesting(
    bases=(CHAMELEON_FIXTURE,),
    name="ftw.chameleon:functional")
