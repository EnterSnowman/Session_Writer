VIDEO_SOURCE_TYPE = 'video'
TABLE_SOURCE_TYPE = 'table'

class BaseSource:
    def __init__(self, name, type_of_source, **params):
        self.name = name
        self.type_of_source = type_of_source
        for k, v in params.items():
            setattr(self, k, v)
