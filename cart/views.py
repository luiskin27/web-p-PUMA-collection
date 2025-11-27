# cart/views.py

# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .forms import CartAddProductForm

def login_required_view(request):
    messages.warning(request, "Войдите в аккаунт, чтобы добавить товар в корзину")
    return redirect(f"/login/?next={request.path}")

@login_required(login_url='/login/')
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')

    if not size:
        messages.error(request, "Выберите размер!")
        return redirect(product.get_absolute_url())

    cart.add(product=product, size=size)
    messages.success(request, f"{product.name} (размер {size}) добавлен в корзину!")

    # ← ВОТ ГЛАВНОЕ: возвращаемся туда, откуда пришли
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_not_found'))


def cart_remove(request, key):
    cart = Cart(request)
    cart.remove(key)
    messages.success(request, "Товар удалён из корзины")
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_clear(request):
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