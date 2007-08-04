import zope.app.publisher.browser
import zope.component

from zope.component.testing import setUp
from zope.configuration.xmlconfig import XMLConfig

import plone.transforms


def configurationSetUp(self):
    setUp()
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('meta.zcml', zope.app.publisher.browser)()
    XMLConfig('configure.zcml', plone.transforms)()