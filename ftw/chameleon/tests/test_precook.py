from ftw.chameleon.precook import precook_templates
from ftw.chameleon.tests import FunctionalTestCase


class TestPrecookTemplates(FunctionalTestCase):

    def test_precooks_instantiated_templates(self):
        view = self.build_view()
        self.assertFalse(self.is_view_template_cooked(view))
        precook_templates()
        self.assertTrue(self.is_view_template_cooked(view))

    def is_view_template_cooked(self, view):
        return bool(view.template.im_func._v_program)
