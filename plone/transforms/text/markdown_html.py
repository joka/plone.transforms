"""
Uses the http://www.freewisdom.org/projects/python-markdown/ module to do its
handy work

Based on work from: Tom Lazar <tom@tomster.org> at the archipelago sprint 2006

"""
from zope.interface import implements

from plone.transforms.interfaces import ITransform
from plone.transforms.message import PloneMessageFactory as _
from plone.transforms.transform import Transform

HAS_MARKDOWN = True
try:
    from markdown import markdown
except ImportError:
    HAS_MARKDOWN = False


class MarkdownTransform(Transform):
    """A transform which transforms markdown text into HTML.

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(ITransform, MarkdownTransform)
      True
    """

    implements(ITransform)

    name = u'plone.transforms.text.markdown_html.MarkdownTransform'
    title = _(u'title_markdown_transform',
              default=u'Markdown to HTML transform')
    description = _(u'description_markdown_transform',
                  default=u"A transform which transforms any markdown text "
                           "into HTML.")

    inputs  = ("text/x-web-markdown",)
    output = "text/html"

    def transform(self, data):
        html = markdown(u''.join(data).encode('utf-8'))
        return (d for d in html.decode('utf-8'))