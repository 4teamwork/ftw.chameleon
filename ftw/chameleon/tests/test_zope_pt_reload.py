from ftw.chameleon.tests import FunctionalTestCase
from ftw.testing import IS_PLONE_5
import os


class TestZopePageTemplateReloadsCanBeDisabled(FunctionalTestCase):

    def setUp(self):
        super(TestZopePageTemplateReloadsCanBeDisabled, self).setUp()
        self.events = self.register_template_compilation_subscriber()

    if not IS_PLONE_5:
        # The CHAMELEON_RELOAD option is required on Plone 4 to disable
        # template reloads; test that it works

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
    else:
        # The CHAMELEON_RELOAD option is removed on Plone 5. To check that's
        # safe, test that Plone 5 disables template reloads in production

        def test_reloads_in_debug_mode(self):
            self.set_plone5_debug_mode(True)
            self.reload_config()
            view = self.build_view()
            view()
            self.events[:] = []
            view.touch_template()
            view()
            self.assertTrue(self.events)

        def test_no_reloads_in_production_mode(self):
            self.set_plone5_debug_mode(False)
            self.reload_config()
            view = self.build_view()
            view()
            self.events[:] = []
            view.touch_template()
            view()
            self.assertFalse(self.events)
