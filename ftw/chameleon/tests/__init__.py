from ftw.chameleon.testing import CHAMELEON_FUNCTIONAL
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from unittest2 import TestCase
import os
import transaction


class FunctionalTestCase(TestCase):
    layer = CHAMELEON_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.load_zcml_string = self.layer['load_zcml_string']
        self.reset_chameleon_environment_variables()

    def tearDown(self):
        self.reset_chameleon_environment_variables()

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()

    def reset_chameleon_environment_variables(self):
        for name in os.environ.keys()[:]:
            if name.startswith('CHAMELEON_'):
                os.environ.pop(name)

        self.reload_config()

    def reload_config(self):
        import chameleon.config
        reload(chameleon.config)
        import ftw.chameleon.config
        reload(ftw.chameleon.config)

    def trigger_foo_template_cooking(self):
        class FooView(BrowserView):
            def __call__(self):
                return ViewPageTemplateFile('templates/foo.pt')(self)
        return FooView(self.portal, self.request)()
