from .basket import Basket


def basket(request):
    # print(Basket(request))
    return {'basket': Basket(request)}