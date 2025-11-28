# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .cart import Cart


@login_required(login_url='/login/')
@require_POST
def cart_add(request, product_id):
    # Проверка: только Покупатели и Администраторы могут добавлять в корзину
    allowed_groups = ['Покупатели', 'Администраторы']
    if not request.user.groups.filter(name__in=allowed_groups).exists():
        messages.error(request, "У вас нет прав добавлять товары в корзину.")
        return redirect('/')

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')

    if not size:
        messages.error(request, "Пожалуйста, выберите размер!")
        return redirect(product.get_absolute_url())

    cart.add(product=product, size=size)
    messages.success(request, f"{product.name} (размер {size}) добавлен в корзину!")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login/')
def cart_remove(request, key):
    allowed_groups = ['Покупатели', 'Администраторы']
    if not request.user.groups.filter(name__in=allowed_groups).exists():
        messages.error(request, "Доступ запрещён.")
        return redirect('/')

    cart = Cart(request)
    cart.remove(key)
    messages.success(request, "Товар удалён из корзины")
    return redirect('cart:cart_detail')


@login_required(login_url='/login/')
def cart_detail(request):
    # КЛЮЧЕВАЯ ПРОВЕРКА — только разрешённые группы видят корзину
    allowed_groups = ['Покупатели', 'Администраторы']
    if not request.user.groups.filter(name__in=allowed_groups).exists():
        messages.error(request, "У вас нет доступа к корзине.")
        return redirect('/')

    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required(login_url='/login/')
def cart_clear(request):
    allowed_groups = ['Покупатели', 'Администраторы']
    if not request.user.groups.filter(name__in=allowed_groups).exists():
        messages.error(request, "Доступ запрещён.")
        return redirect('/')

    cart = Cart(request)
    cart.clear()
    messages.success(request, "Корзина очищена")
    return redirect('cart:cart_detail')
    










# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     size = request.POST.get('size')
    
#     if not size:
#         messages.error(request, "Выберите размер!")
#         return redirect(product.get_absolute_url())
        
#     cart.add(product=product, size=size)
#     messages.success(request, f"{product.name} ({size}) добавлен в корзину!")
#     return redirect('cart:cart_detail')

# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
# from shop.models import Product
# from .cart import Cart
# from django.contrib import messages


# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     size = request.POST.get('size')
    
#     if not size:
#         messages.error(request, "Пожалуйста, выберите размер!")
#         return redirect(product.get_absolute_url())
        
#     cart.add(product=product, size=size)
#     messages.success(request, f"{product.name} ({size}) добавлен в корзину!")
#     return redirect('cart:cart_detail')


# def cart_remove(request, key):
#     cart = Cart(request)
#     cart.remove(key)
#     return redirect('cart:cart_detail')


# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/detail.html', {'cart': cart})