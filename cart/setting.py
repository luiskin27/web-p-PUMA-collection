# === КОРЗИНА ===
CART_SESSION_ID = 'cart'

# Добавляем контекст-процессор корзины
from cart.context_processors import cart  # ← можно без этого, главное строка ниже
TEMPLATES[0]['OPTIONS']['context_processors'].append('cart.context_processors.cart')