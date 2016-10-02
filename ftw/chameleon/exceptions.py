

class TemplateCookedUnexpectedly(Exception):
    """A template unexpectedly cooked.
    """

    def __init__(self, msg, template_path):
        self.template_path = template_path
        super(TemplateCookedUnexpectedly, self).__init__(msg)
