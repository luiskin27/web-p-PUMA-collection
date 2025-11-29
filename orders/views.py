# orders/views.py
# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# from django.http import HttpResponse
# from django.contrib.admin.views.decorators import staff_member_required
# from django.urls import reverse
# from django.utils.html import format_html
# import weasyprint
# from io import BytesIO

from .forms import OrderCreateForm
from cart.cart import Cart
from .models import Order, OrderItem


@login_required(login_url='/login/')
def order_create(request):
    cart = Cart(request)

    # Проверка групп — оставляем как у тебя было
    allowed_groups = ['Покупатели', 'admin']
    if not request.user.groups.filter(name__in=allowed_groups).exists():
        messages.error(request, "У вас нет прав для оформления заказа.")
        return redirect('/')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Сохраняем товары
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    size=item['size']
                )

            cart.clear()

            # # ГЕНЕРАЦИЯ PDF
            # html = render_to_string('orders/order/pdf.html', {'order': order})
            # out = BytesIO()
            # weasyprint.HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(out)
            # pdf_file = out.getvalue()

            # # ОТПРАВКА ПИСЬМА ПОКУПАТЕЛЮ
            subject = f'PUMA – Заказ №{order.id} оформлен'
            email_body = render_to_string('orders/order/email.txt', {'order': order})

            email = EmailMessage(
                subject=subject,
                body=email_body,
                from_email='PUMA Shop <noreply@puma-shop.com>',
                to=[order.email],
                reply_to=['support@puma-shop.com'],
            )
            # email.attach(f'PUMA_Order_{order.id}.pdf', pdf_file, 'application/pdf')
            email.send()

            messages.success(request, f"Заказ №{order.id} успешно оформлен и отправлен на почту!")
            return render(request, 'orders/created.html', {'order': order})

    else:
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


# PDF для админа (кнопка в админке)
# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html', {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="puma_order_{order.id}.pdf"'
#     weasyprint.HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(response)
#     return response



















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