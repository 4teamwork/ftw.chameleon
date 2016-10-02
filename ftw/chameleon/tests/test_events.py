from chameleon.template import BaseTemplate
from ftw.chameleon.tests import FunctionalTestCase
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import os


EVENTS = []


def compiling_template_event_subscriber(event):
    EVENTS.append(event)


class TestCompilingTemplateEvent(FunctionalTestCase):

    def test_event_is_fired(self):
        self.load_zcml_string('''
        <configure xmlns="http://namespaces.zope.org/zope">
          <subscriber
            for="ftw.chameleon.interfaces.ICompilingTemplateEvent"
            handler="{}.compiling_template_event_subscriber"
            />
        </configure>
        '''.format(type(self).__module__))
        template = ViewPageTemplateFile('templates/foo.pt')

        class FooView(BrowserView):
            def __call__(self):
                return template(self)

        self.assertEquals('<h1> Hello World</h1>',
                          FooView(self.portal, self.request)().strip())

        event = EVENTS.pop()
        self.assertEquals('foo.pt', os.path.basename(event.template_path))
        self.assertTrue(isinstance(event.template, BaseTemplate))
