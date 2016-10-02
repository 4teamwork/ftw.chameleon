from ftw.chameleon.tests import FunctionalTestCase
import os


class TestZopePageTemplateSupportsReloadOption(FunctionalTestCase):

    def setUp(self):
        super(TestZopePageTemplateSupportsReloadOption, self).setUp()
        self.events = self.register_template_compilation_subscriber()

    def test_reloads_when_reload_option_enabled(self):
        os.environ['CHAMELEON_RELOAD'] = 'true'
        self.reload_config()
        view = self.build_view()
        view()
        self.events[:] = []
        view.touch_template()
        view()
        self.assertTrue(self.events)

    def test_no_reloads_when_reload_option_disabled(self):
        os.environ['CHAMELEON_RELOAD'] = 'false'
        self.reload_config()
        view = self.build_view()
        view()
        self.events[:] = []
        view.touch_template()
        view()
        self.assertFalse(self.events)
