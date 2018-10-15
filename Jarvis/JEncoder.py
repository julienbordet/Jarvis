from json import JSONEncoder

class JEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'jsonable'):
            return o.jsonable()
        else:
            raise TypeError("Object of type {0} with value of {0} is not JSON serializable".format(type(o),
                                                                                                   repr(o)))