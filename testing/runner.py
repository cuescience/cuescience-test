from django.db.models import AutoField
from django.test.runner import DiscoverRunner


class GlobalUniqueAutoField(object):
    counter = 0

    @classmethod
    def get_id(cls):
        id = cls.counter
        cls.counter += 1
        return id


class CuescienceTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super(CuescienceTestRunner, self).setup_test_environment(**kwargs)
        from django.db import models

        ms = models.get_models(include_auto_created=True)
        for model in ms:
            pk_field = model._meta.pk
            if isinstance(pk_field, AutoField):
                pk_field.default = GlobalUniqueAutoField.get_id
            else:
                # TODO use the logger here
                print ("The model {0} uses a {1} pk field!".format(model, type(pk_field)))

    def teardown_test_environment(self):
        GlobalUniqueAutoField.counter = 0
        super(CuescienceTestRunner, self).teardown_test_environment()
