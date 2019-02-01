"""

VIDEO_SOURCE_TYPE : str
    String identifier for video data sources.

TABLE_SOURCE_TYPE : str
    String identifier for table data sources.

"""

VIDEO_SOURCE_TYPE = 'video'
TABLE_SOURCE_TYPE = 'table'


class BaseSource:
    """

    Base class for objects, which stores information about data source.

    Attributes
    ----------
    name : str
        Name of data source
    type_of_source : str
        Type of data source.

    """
    def __init__(self, name, type_of_source, **params):
        """

        Initializes base object for data source information.

        Parameters
        ----------
        name : str
            Name of data source
        type_of_source : str
            Type of data source.
        **params
            Arbitrary keyword arguments. Stores additional information about data source.
        """
        self.name = name
        self.type_of_source = type_of_source
        for k, v in params.items():
            setattr(self, k, v)
