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
        import chameleon
        reload(chameleon.config)
        reload(chameleon.compiler)
        reload(chameleon.exc)
        reload(chameleon.template)
        import ftw.chameleon.config
        reload(ftw.chameleon.config)

    def build_view(self, template_path='templates/foo.pt'):
        class View(BrowserView):
            template = ViewPageTemplateFile(template_path)

            def __call__(self):
                return self.template(self)

            def touch_template(self):
                mtime = os.path.getmtime(self.template.filename)
                mtime += 1
                os.utime(self.template.filename, (mtime, mtime))

        return View(self.portal, self.request)

    def trigger_foo_template_cooking(self):
        return self.build_view()()

    def register_template_compilation_subscriber(self):
        event_list = []

        def subscriber(event):
            event_list.append(event)

        globals()['_event_subscriber'] = subscriber
        self.load_zcml_string('''
            <configure xmlns="http://namespaces.zope.org/zope">
              <subscriber
                for="ftw.chameleon.interfaces.ICompilingTemplateEvent"
                handler="{}._event_subscriber"
                />
            </configure>
            '''.format(FunctionalTestCase.__module__))
        del globals()['_event_subscriber']
        return event_list
