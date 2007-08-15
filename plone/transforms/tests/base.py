from os.path import abspath, dirname, join
from unittest import TestCase

from zope.component import queryUtility

from plone.transforms.interfaces import ITransform
from plone.transforms.interfaces import ITransformResult
from plone.transforms.tests.layer import TransformLayer


def input_file_path(file_, name):
    return join(abspath(dirname(file_)), 'input', name)


class TransformTestCase(TestCase):

    layer = TransformLayer

    name = None
    class_ = None
    input_ = None
    output = None

    def test_registration(self):
        util = queryUtility(ITransform, name=self.name)
        self.failIf(util is None)
        self.failUnless(isinstance(util, self.class_))

    def test_invalid_transform(self):
        util = queryUtility(ITransform, name=self.name)
        result = util.transform(None)
        self.failUnless(result is None)

    def test_transform(self):
        util = queryUtility(ITransform, name=self.name)
        result = util.transform(self.input_)

        # Make sure we got back a proper result
        self.failUnless(ITransformResult.providedBy(result))
        self.failUnless(result.errors is None)

        # Did we get an iterator as the primary result data?
        self.failUnless(getattr(result.data, 'next', None) is not None)

        # Check the beginning of the output only
        result_string = ''.join(result.data)
        self.failUnless(result_string.startswith(self.output))
