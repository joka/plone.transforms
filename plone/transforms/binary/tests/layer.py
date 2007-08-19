import zope.component
from zope.component.testing import setUp
from zope.component.testing import tearDown

from zope.configuration.xmlconfig import XMLConfig

import plone.transforms.image


class BinaryLayer:

    @classmethod
    def setUp(cls):
        setUp()
        XMLConfig('meta.zcml', zope.component)()
        XMLConfig('configure.zcml', plone.transforms.binary)()

    @classmethod
    def tearDown(cls):
        tearDown()
