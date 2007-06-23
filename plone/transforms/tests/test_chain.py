# -*- coding: UTF-8 -*-
"""
    Tests for transformation chains.
"""

import unittest

import plone.transforms
from plone.transforms.interfaces import ITransform
from plone.transforms.interfaces import ITransformChain
from plone.transforms.chain import TransformChain
from plone.transforms.transform import Transform

import zope.component
from zope.component import getGlobalSiteManager
from zope.component import queryUtility
from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig
from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite


class TestChain(TransformChain):

    name = u"test"
    title = u"Test chain"


class ReverseTransform(Transform):

    name = u"plone.transforms.test_chain.ReverseTransform"
    title = u"Reversing transform."

    def transform(self, data):
        temp = [d for d in data]
        temp.reverse()
        return (d for d in temp)


def configurationSetUp(self):
    setUp()
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('configure.zcml', plone.transforms)()


def testEmptyChain():
    """
    First we create and register a new transform chain:
    
      >>> gsm = getGlobalSiteManager()
      >>> gsm.registerUtility(TestChain(),
      ...     ITransformChain,
      ...     name='EmptyChain')

      >>> chain = queryUtility(ITransformChain,
      ...            name='EmptyChain')
      >>> type(chain)
      <class 'plone.transforms.tests.test_chain.TestChain'>

      >>> chain.name
      u'test'

    Set up some test text and turn it into a generator which fullfils the
    iterator protocol:

      >>> text = u"Some simple test text."
      >>> data = (chr for chr in text)

    Now transform the data:

      >>> result = chain.transform(data)

    Check the result:

      >>> result
      <generator object at ...>

      >>> u''.join(result) == text
      True
    """


def testIdenticalChain():
    """
    First we create a new transform chain:

      >>> chain = TestChain()
      >>> chain.title = u'Identity chain'

    Then put in two transforms:

      >>> identity = ('plone.transforms.interfaces.ITransform', 
      ...             'plone.transforms.identity.IdentityTransform')

      >>> chain.append(identity)
      >>> chain.append(identity)

    And register the new chain:

      >>> gsm = getGlobalSiteManager()
      >>> gsm.registerUtility(chain,
      ...     ITransformChain,
      ...     name='IdenticalChain')

    Make sure we got the right chain:

      >>> chain = queryUtility(ITransformChain,
      ...            name='IdenticalChain')
      >>> type(chain)
      <class 'plone.transforms.tests.test_chain.TestChain'>
      >>> chain.title
      u'Identity chain'
      >>> len(chain)
      2

    Set up some test text and turn it into a generator which fullfils the
    iterator protocol:

      >>> text = u"Some simple test text."
      >>> data = (chr for chr in text)

    Now transform the data and check the result:

      >>> result = chain.transform(data)
      >>> u''.join(result) == text
      True
    """


def testReversingChain():
    """
    First we need to load the ReverseTransform:

      >>> XMLConfig('configure.zcml', plone.transforms.tests)()

    Then create a new transform chain:

      >>> chain = TestChain()
      >>> chain.name = u'ReverseChain'
      >>> chain.title = u'Reversing chain'

    Put in one transforms:

      >>> reverse = ('plone.transforms.interfaces.ITransform', 
      ...            'plone.transforms.test_chain.ReverseTransform')

      >>> chain.append(reverse)

    And register the new chain:

      >>> gsm = getGlobalSiteManager()
      >>> gsm.registerUtility(chain,
      ...     ITransformChain,
      ...     name='ReverseChain')

    Make sure we got the right chain:

      >>> chain = queryUtility(ITransformChain,
      ...            name='ReverseChain')
      >>> type(chain)
      <class 'plone.transforms.tests.test_chain.TestChain'>
      >>> chain.title
      u'Reversing chain'
      >>> len(chain)
      1

    Set up some test text and turn it into a generator which fullfils the
    iterator protocol:

      >>> text = u"ABCDE"
      >>> data = (chr for chr in text)

    Now transform the data and check the result:

      >>> result = chain.transform(data)
      >>> u''.join(result)
      u'EDCBA'

    Add another reverse transform to the chain:

      >>> chain.append(reverse)

    And transform the text again:

      >>> text = u"ABCDE"
      >>> data = (chr for chr in text)

      >>> result = chain.transform(data)
      >>> u''.join(result)
      u'ABCDE'
    """


def testReversingSplitChain():
    """
    First we need to load ReverseTransform and SplitTransform:

      >>> XMLConfig('configure.zcml', plone.transforms.tests)()

    Then create a new transform chain:

      >>> chain = TestChain()
      >>> chain.name = u'ReverseSplitChain'
      >>> chain.title = u'Reversing and splitting chain'

    Put in one transforms:

      >>> reverse = ('plone.transforms.interfaces.ITransform', 
      ...            'plone.transforms.test_chain.ReverseTransform')

      >>> split = ('plone.transforms.interfaces.IMultipleOutputTransform',
      ...          'plone.transforms.test_transform.SplitTransform')

      >>> chain.append(reverse)
      >>> chain.append(split)

    And register the new chain:

      >>> gsm = getGlobalSiteManager()
      >>> gsm.registerUtility(chain,
      ...     ITransformChain,
      ...     name='ReverseSplitChain')

    Make sure we got the right chain:

      >>> chain = queryUtility(ITransformChain,
      ...            name='ReverseSplitChain')
      >>> type(chain)
      <class 'plone.transforms.tests.test_chain.TestChain'>
      >>> chain.title
      u'Reversing and splitting chain'
      >>> len(chain)
      2

    Set up some test text and turn it into a generator:

      >>> text = u"ABCDEFG"
      >>> data = (chr for chr in text)

    Now transform the data and check the result:

      >>> result = chain.transform(data)
      >>> result
      {'default': <generator object at ...>, 'second': <generator object at ...}

      >>> default = result.get('default')
      >>> u''.join(default)
      u'GECA'

      >>> second = result.get('second')
      >>> u''.join(second)
      u'FDB'

    Reverse the order of the two transforms in the chain:
    
      >>> chain.reverse()
    
    And transform the text again:
    
      >>> text = u"ABCDEFG"
      >>> data = (chr for chr in text)

      >>> result = chain.transform(data)
      >>> result
      <generator object at ...>
      
      >>> u''.join(result)
      u'GECA'
    """


def test_suite():
    return unittest.TestSuite((
        DocTestSuite('plone.transforms.chain'),
        DocTestSuite(setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | 
                                 doctest.NORMALIZE_WHITESPACE),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
