from .models import Cart


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

def mini_cart(request):
    if request.user.is_authenticated:
        cart = get_or_create_cart(request.user)
        items = cart.cart_detatils.select_related('product')
        total = sum(item.total_price for item in items)
        total_count = sum(item.quantity for item in items)
        return {
            'mini_cart_items': items,
            'mini_cart_total': total,
            'mini_cart_count': total_count
        }
    return {
        'mini_cart_items': [],
        'mini_cart_total': 0
    }
