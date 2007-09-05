"""
Uses Roberto A. F. De Almeida's http://dealmeida.net/ module to do its
handy work

Based on work from: Tom Lazar <tom@tomster.org> at the archipelago sprint 2006.
"""
from zope.interface import implements

from plone.transforms.interfaces import ITransform
from plone.transforms.message import PloneMessageFactory as _
from plone.transforms.stringiter import StringIter
from plone.transforms.transform import Transform
from plone.transforms.transform import TransformResult

HAS_TEXTILE = True
try:
    from textile import textile
except ImportError:
    HAS_TEXTILE = False


class TextileTransform(Transform):
    """A transform which transforms textile text into HTML."""

    implements(ITransform)

    name = u'plone.transforms.text.textile_html.TextileTransform'

    title = _(u'title_textile_transform',
        default=u'Textile to HTML transform')

    inputs  = ("text/x-web-textile",)
    output = "text/html"

    available = False

    def __init__(self):
        super(TextileTransform, self).__init__()
        if HAS_TEXTILE:
            self.available = True

    def transform(self, data):
        """Returns the transform result."""
        if self._validate(data) is None:
            return None

        html = textile(u''.join(data).encode('utf-8'), encoding='utf-8', output='utf-8')
        return TransformResult(StringIter(unicode(html, 'utf-8')))