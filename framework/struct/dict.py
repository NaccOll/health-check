def _create(value):
    if value is not None and isinstance(value, list):
        return list(map(lambda x: _create(x), value))
    return Dict.create(value) if isinstance(value, dict) else value


class Dict(dict):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            tmp = Dict()
            self[key] = tmp
            return tmp

    def __setattr__(self, key, value):
        self[key] = _create(value)

    def get_prefix(self, prefix: str):
        args_arr = prefix.split(".")
        if len(args_arr) == 1:
            return _create(self.__getattr__(args_arr[0]))
        for (index, arg) in enumerate(args_arr):
            if index == 0:
                result = _create(self.__getattr__(arg))
                continue
            if arg not in result:
                return None
            result = _create(result[arg])
        return _create(result)

    def update(self, d):
        for key in d.keys():
            self[key] = _create(d[key])

    def is_useless(self):
        return self.keys() == 0

    @staticmethod
    def create(dict_value):
        result = Dict()
        result.update(dict_value)
        return result
