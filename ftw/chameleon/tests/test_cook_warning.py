from ftw.chameleon import precook
from ftw.chameleon.tests import FunctionalTestCase
from testfixtures import LogCapture
import os


class TestCookWarning(FunctionalTestCase):

    def setUp(self):
        super(TestCookWarning, self).setUp()
        precook.SKINS_PRECOOKED_FOR_SITES[:] = [
            '/'.join(self.portal.getPhysicalPath())]

    def test_warning_logged_in_eager_mode(self):
        os.environ['CHAMELEON_EAGER'] = 'true'
        os.environ['FTW_CHAMELEON_RECOOK_WARNING'] = 'true'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log_entry = ('ftw.chameleon',
                     'WARNING',
                     "Template '{}/templates/foo.pt' was unexpectedly cooked while"
                     " eager loading is enabled.".format(
                         os.path.dirname(__file__)))
        log.check(log_entry, log_entry)

    def test_no_warning_if_warning_disabled(self):
        os.environ['CHAMELEON_EAGER'] = 'true'
        os.environ['FTW_CHAMELEON_RECOOK_WARNING'] = 'false'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log.check()

    def test_no_warning_logged_in_non_eager_mode(self):
        os.environ['CHAMELEON_EAGER'] = 'false'
        os.environ['FTW_CHAMELEON_RECOOK_WARNING'] = 'true'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log.check()

    def test_no_warning_logged_in_auto_reload_mode(self):
        os.environ['CHAMELEON_EAGER'] = 'true'
        os.environ['CHAMELEON_RELOAD'] = 'true'
        os.environ['FTW_CHAMELEON_RECOOK_WARNING'] = 'true'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log.check()


class TestCookException(FunctionalTestCase):

    def setUp(self):
        super(TestCookException, self).setUp()
        precook.SKINS_PRECOOKED_FOR_SITES[:] = [
            '/'.join(self.portal.getPhysicalPath())]

    def test_exception_logged_in_eager_mode(self):
        os.environ['CHAMELEON_EAGER'] = 'true'
        os.environ['FTW_CHAMELEON_RECOOK_EXCEPTION'] = 'true'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log_entry = ('ftw.chameleon',
                     'ERROR',
                     "Template '{}/templates/foo.pt' was unexpectedly cooked while"
                     " eager loading is enabled.".format(
                         os.path.dirname(__file__)))
        log.check(log_entry, log_entry)

    def test_no_exception_if_exception_disabled(self):
        os.environ['CHAMELEON_EAGER'] = 'true'
        os.environ['FTW_CHAMELEON_RECOOK_EXCEPTION'] = 'false'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log.check()

    def test_no_exception_logged_in_non_eager_mode(self):
        os.environ['CHAMELEON_EAGER'] = 'false'
        os.environ['FTW_CHAMELEON_RECOOK_EXCEPTION'] = 'true'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log.check()

    def test_no_exception_logged_in_auto_reload_mode(self):
        os.environ['CHAMELEON_EAGER'] = 'true'
        os.environ['CHAMELEON_RELOAD'] = 'true'
        os.environ['FTW_CHAMELEON_RECOOK_EXCEPTION'] = 'true'
        self.reload_config()

        with LogCapture() as log:
            self.trigger_foo_template_cooking()

        log.check()
