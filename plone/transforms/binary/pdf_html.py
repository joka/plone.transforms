from zope.interface import implements

from plone.transforms.interfaces import IPipeTransform
from plone.transforms.message import PloneMessageFactory as _
from plone.transforms.pipe import PipeTransform
from plone.transforms.transform import TransformResult
from plone.transforms.utils import html_bodyfinder


class PDFTransform(PipeTransform):
    """A transform which transforms pdf into HTML.

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(IPipeTransform, PDFTransform)
      True
    """

    implements(IPipeTransform)

    name = u'plone.transforms.binary.pdf_html.PDFTransform'

    title = _(u'title_pdf_html_transform',
        default=u'PDF to HTML transform')

    description = _(u'description_pdf_html_transform',
        default=u"A transform which transforms PDF into HTML.")

    inputs  = ("application/pdf",)
    output = "text/html"

    command = 'pdftohtml'
    args = "%(infile)s -noframes -stdout -enc UTF-8"
    use_stdin = False

    def extractOutput(self, stdout):
        return html_bodyfinder(stdout.read()).decode('utf-8', 'ignore')
