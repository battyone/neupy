from abc import abstractmethod

from neupy.core.config import Configurable, ConfigurableABC
from neupy.core.properties import Property

from base import BaseTestCase


class ConfigsTestCase(BaseTestCase):
    def test_configuration_inheritance(self):
        class A(Configurable):
            property_a = Property()

        class B(A):
            property_b = Property()

        class C(B):
            property_c = Property()

        class D(A):
            property_d = Property()

        self.assertEqual(sorted(A.options.keys()), ['property_a'])
        self.assertEqual(sorted(B.options.keys()),
                         ['property_a', 'property_b'])
        self.assertEqual(sorted(D.options.keys()),
                         ['property_a', 'property_d'])
        self.assertEqual(sorted(C.options.keys()),
                         ['property_a', 'property_b', 'property_c'])

    def test_invalid_configs_setup(self):
        class A(Configurable):
            correct_property = Property()

        a = A(correct_property=3)
        with self.assertRaises(ValueError):
            a = A(invalid_property=3)

    def test_abc_config(self):
        class A(ConfigurableABC):
            @abstractmethod
            def important_method(self):
                pass

        class InheritA(A):
            pass

        with self.assertRaises(TypeError):
            InheritA()
