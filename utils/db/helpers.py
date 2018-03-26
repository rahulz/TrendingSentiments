def cleanup_fields(d, model):
    fields = model._meta.get_fields()
    ret_d = {}
    for field in fields:
        if field.name in d.keys():
            ret_d[field.name] = d[field.name]
    return ret_d
