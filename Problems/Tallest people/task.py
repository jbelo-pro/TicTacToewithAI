def tallest_people(**kwargs):

    n = sorted(kwargs, key=kwargs.get, reverse=True)
    tall = -1
    tallest = []
    for name in n:
        if kwargs[name] >= tall:
            tallest.append(name)
            tall = kwargs[name]
        else:
            break
    tallest.sort()
    for name in tallest:
        print('{0} : {1}'.format(name, kwargs[name]))