from zope.interface import Attribute, Interface


class ITransformResult(Interface):
    """Data stream, is the result of a transform.
    
    The data argument takes an object providing Python's iterator protocol.
    In case of textual data, the data has to be Unicode. The same applies
    to the data return value and the values in the subobjects
    """

    data = Attribute("The default return data from the transform.")

    metadata = Attribute("The metadata for the result as a dictonary.")

    subobjects = Attribute("A dict of subobject keys and subobjects."
                         "The values should be iterators as well.")


class ITransform(Interface):
    """A transformation utility.
    """

    inputs = Attribute("List of mimetypes this transform accepts as inputs. "
                       "Mimetypes syntax follows rfc2045 / rfc4288.")

    output = Attribute("Mimetype this transform outputs. Mimetypes syntax "
                       "follows rfc2045 / rfc4288.")

    name = Attribute("A unique name for the transform.")

    title = Attribute("The title of the transform.")

    description = Attribute("A description of the transform.")

    def transform(data):
        """
        The transform method takes some data in one of the input formats and
        returns an ITransformResult in the output format.
        """
