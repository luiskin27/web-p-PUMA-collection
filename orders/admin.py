# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'email', 'city', 'created', 'paid']
    list_filter = ['paid', 'created']
    search_fields = ['first_name', 'email']

    # ← НОВАЯ КНОПКА В АДМИНКЕ
    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.title = "Заказы PUMA"

        columns = ['ID', 'Имя', 'Email', 'Город', 'Дата', 'Сумма', 'Оплачено']
        ws.append(columns)
        for col_num, column_title in enumerate(columns, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = Font(bold=True)

        for order in queryset:
            ws.append([
                order.id,
                f"{order.first_name} {order.last_name}",
                order.email,
                order.city,
                order.created.strftime("%d.%m.%Y %H:%M"),
                order.get_total_cost(),
                "Да" if order.paid else "Нет"
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=puma_orders.xlsx'
        wb.save(response)
        return response

    export_to_excel.short_description = "Экспорт выбранных заказов в Excel"