from chameleon.template import BaseTemplate
from ftw.chameleon.tests import FunctionalTestCase
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

        self.assertEquals('<h1> Hello World</h1>',
                          self.trigger_foo_template_cooking().strip())

        event = EVENTS.pop()
        self.assertEquals('foo.pt', os.path.basename(event.template_path))
        self.assertTrue(isinstance(event.template, BaseTemplate))
