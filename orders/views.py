# orders/views.py
# orders/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem


@login_required(login_url='/login/')
def order_create(request):
    cart = Cart(request)

    # ПРОВЕРКА ГРУППЫ — только Покупатели и Администраторы могут оформлять заказ
    allowed_groups = ['Покупатели', 'Администраторы']
    if not request.user.groups.filter(name__in=allowed_groups).exists():
        messages.error(request, "У вас нет прав для оформления заказа. Обратитесь к администратору.")
        return redirect('/')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # теперь всегда будет пользователь (он залогинен)
            order.save()

            # Сохраняем товары из корзины в заказ
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    size=item['size']
                )

            cart.clear()
            messages.success(request, f"Заказ №{order.id} успешно оформлен!")
            return render(request, 'orders/created.html', {'order': order})

    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})



















# from django.shortcuts import render, redirect
# from .forms import OrderCreateForm
# from cart.cart import Cart
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.views.generic import View

# @login_required(login_url='/login/')
# def order_create(request):
#     cart = Cart(request)

#     allowed_groups = ['Покупатели', 'Администраторы']
#     if not request.user.groups.filter(name__in=allowed_groups).exists():
#         messages.error(request, "У вас нет прав для оформления заказа. Обратитесь к администратору.")
#         return redirect('/')

#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user # if request.user.is_authenticated else None
#             order.save()
#             for item in cart:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item['product'],
#                     price=item['price'],
#                     quantity=item['quantity'],
#                     size=item['size']
#                 )
#             cart.clear()
#             messages.success(request, f"Заказ №{order.id} успешно оформлен!")
#             return render(request, 'orders/created.html', {'order': order})
#     else:
#         form = OrderCreateForm()
#     return render(request, 'orders/create.html', {'cart': cart, 'form': form})