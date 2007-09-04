from logging import DEBUG
from persistent import Persistent
from zope.interface import implements

from plone.transforms.interfaces import ITransform
from plone.transforms.interfaces import ITransformResult
from plone.transforms.log import log

from plone.transforms.message import PloneMessageFactory as _


class TransformResult(object):
    """Data stream, is the result of a transform.
    
    The data argument takes an object providing Python's iterator protocol.
    In case of textual data, the data has to be Unicode. The same applies
    to the data return value and the values in the subobjects

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(ITransformResult, TransformResult)
      True
    """

    implements(ITransformResult)

    data = None
    metadata = None
    subobjects = None
    errors = None

    def __init__(self, data, metadata=None, subobjects=None, errors=None):
        self.data = data
        self.errors = errors
        if subobjects is not None:
            self.subobjects = subobjects
        else:
            self.subobjects = {}
        if metadata is not None:
            self.metadata = metadata
        else:
            self.metadata = {}


class Transform(object):
    """A transform is an utility.

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(ITransform, Transform)
      True
    """

    implements(ITransform)

    inputs = (None, )
    output = None

    name = u'plone.transforms.transform.Transform'
    title = _(u'title_skeleton_transform',
              default=u'A skeleton transform.')
    description = None

    available = True

    def __init__(self):
        super(Transform, self).__init__()

    def _validate(self, data):
        """Checks if the transform itself is available and the passed in data
        is of the right type.
        """
        if not self.available:
            return None
        # Invalid input
        if data is None:
            log(DEBUG, "No input while transforming data in %s." % self.name)
            return None
        elif isinstance(data, basestring):
            log(DEBUG, "Invalid input while transforming data in %s." %
                        self.name)
            return None
        return True

    def transform(self, data):
        """The transform method takes some data in one of the input formats and
        returns it in the output format.

        The data argument takes an object providing Python's iterator protocol.
        In case of textual data, the data has to be Unicode. The same applies
        to the return value.
        """
        if self._validate(data) is None:
            return None

        return TransformResult(data)


class PersistentTransform(Transform, Persistent):
    """A persistent transform is an utility with optional configuration
    information.

    Let's make sure that this implementation actually fulfills the API.

      >>> from zope.interface.verify import verifyClass
      >>> verifyClass(ITransform, PersistentTransform)
      True
    """

    implements(ITransform)

    inputs = (None, )
    output = None

    name = u'plone.transforms.transform.PersistentTransform'
    title = _(u'title_skeleton_transform',
              default=u'A skeleton transform.')
    description = None

    available = True
