class NoInstancesMeta(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")
