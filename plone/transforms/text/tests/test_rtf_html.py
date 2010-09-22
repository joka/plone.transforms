# -*- coding: UTF-8 -*-
"""
    Tests for the rtf transform.
"""

from unittest import TestSuite, makeSuite

from plone.transforms.interfaces import ITransform
from plone.transforms.tests.base import TransformTestCase
from plone.transforms.text.rtf_html import RTFTransform, HAS_PYTH

TESTDATA=u"""{\\rtf1\\mac\\ansicpg10000\\cocoartf824\\cocoasubrtf420\n{\\fonttbl\\f0\\fswiss\\fcharset77 Helvetica;}this{\obj } is a {\pict ff}test{\*\shppict {\pict\picscalex35\picscaley35\piccropl0\piccropr0\piccropt0\piccropb0\picw2048\pich1360\picwgoal24576\pichgoal16320\jpegblip
540048000000010000004800000001000000323030393a30373a32392031313a32353a33340017009a82050001000000f40100009d82050001000000fc010000}}}"""

class RTFTransformTest(TransformTestCase):

    name = 'plone.transforms.text.rtf_html.RTFTransform'
    class_ = RTFTransform
    interface = ITransform
    input_ = iter(TESTDATA)
    output = u'<div><p>this is a test</p></div>'

def test_suite():
    suite = TestSuite()
    if HAS_PYTH:
        suite.addTest(makeSuite(RTFTransformTest))
    return suite
