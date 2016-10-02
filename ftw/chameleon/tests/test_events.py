from chameleon.template import BaseTemplate
from ftw.chameleon.tests import FunctionalTestCase
import os


class TestCompilingTemplateEvent(FunctionalTestCase):

    def test_event_is_fired(self):
        events = self.register_template_compilation_subscriber()
        self.assertEquals('<h1> Hello World</h1>',
                          self.trigger_foo_template_cooking().strip())

        event = events.pop()
        self.assertEquals('foo.pt', os.path.basename(event.template_path))
        self.assertTrue(isinstance(event.template, BaseTemplate))
