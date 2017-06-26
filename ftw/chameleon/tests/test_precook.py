from ftw.chameleon.precook import eager_load_portal_skins
from ftw.chameleon.precook import precook_templates
from ftw.chameleon.precook import SKINS_PRECOOKED_FOR_SITES
from ftw.chameleon.tests import FunctionalTestCase
from Products.PageTemplates import ZopePageTemplate
import os


class Stub(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestPrecookTemplates(FunctionalTestCase):

    def test_01_precooks_portal_skins_after_first_access(self):
        os.environ['CHAMELEON_EAGER'] = 'true'
        self.reload_config()
        SKINS_PRECOOKED_FOR_SITES[:] = []
        sendto_template = self.portal.portal_skins.plone_templates.sendto_template
        eager_load_portal_skins(Stub(request=Stub(PARENTS=self.portal.aq_chain)))
        self.assertTrue(sendto_template._v_program,
                        'Expected sendto_template to be compiled now.')

    def test_02_precooks_instantiated_templates(self):
        view = self.build_view()
        self.assertFalse(self.is_view_template_cooked(view))
        precook_templates()
        self.assertTrue(self.is_view_template_cooked(view))

    def test_doesnt_precook_persistent_templates(self):
        # Using ZopePageTemplate.manage_addPageTemplateForm as an example of
        # a persistent template here
        template = ZopePageTemplate.manage_addPageTemplateForm
        self.assertIsNone(template._v_program)
        precook_templates()
        self.assertIsNone(template._v_program)

    def is_view_template_cooked(self, view):
        return bool(view.template.im_func._v_program)
