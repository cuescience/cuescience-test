from django.db.models import AutoField
from django.test.runner import DiscoverRunner
from teamcity.unittestpy import TeamcityTestRunner


class GlobalUniqueAutoField(object):
    counter = 0

    @classmethod
    def get_id(cls):
        id = cls.counter
        cls.counter += 1
        return id


class CuescienceTestRunner(DiscoverRunner):
    test_runner = TeamcityTestRunner()
    
    def setup_test_environment(self, **kwargs):
        super(CuescienceTestRunner, self).setup_test_environment(**kwargs)
        from django.db import models
        from django.apps import apps

        ms = apps.get_models(include_auto_created=True)
        self.unmanaged_models = []
        for model in ms:
            # Change unmanaged models, to managed ones for testing
            if not model._meta.managed:
                self.unmanaged_models.append(model)
                model._meta.managed = True
                model._meta.db_table = "{}_{}".format(model._meta.app_label, model._meta.model_name)
                
            pk_field = model._meta.pk
            if isinstance(pk_field, AutoField):
                pk_field.default = GlobalUniqueAutoField.get_id
            else:
                # TODO use the logger here
                print ("The model {0} uses a {1} pk field!".format(model, type(pk_field)))

    def teardown_test_environment(self):
        GlobalUniqueAutoField.counter = 0
        for m in self.unmanaged_models:
            m._meta.managed = False
        super(CuescienceTestRunner, self).teardown_test_environment()
