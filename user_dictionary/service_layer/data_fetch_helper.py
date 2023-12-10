def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def get_list_or_none(classmodel, **kwargs):
    return classmodel.objects.filter(**kwargs)
