def dict_to_obj(data):
    top = type('tree', (object,), data)
    seqs = tuple, list, set, frozenset
    for i, j in data.items():
        if isinstance(j, dict):
            setattr(top, i, dict_to_obj(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(dict_to_obj(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top
