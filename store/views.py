from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import logging
from .models import Order, OrderTracking

from .models import (
    Product, Category, Order, OrderItem, Review, Wishlist
)
from .forms import ReviewForm
from .models import HeroImage


# --- HOME PAGE ---
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    hero_images = HeroImage.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'store/home.html', {'products': products, 'categories': categories, 'hero_images': hero_images})


# --- ALL PRODUCTS ---
def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/all_products.html', {'products': products, 'categories': categories})


# --- PRODUCT DETAIL ---
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews})


# --- CATEGORY PRODUCTS ---
def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'store/category.html', {'category': category, 'products': products, 'categories': categories})


# --- CART HELPERS ---
def get_cart_items(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id_str, quantity in cart.items():
        try:
            product_id = int(product_id_str)
            product = Product.objects.get(id=product_id)
        except (ValueError, Product.DoesNotExist):
            continue

        subtotal = product.price * quantity
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal

    return items, total


# --- CART VIEWS ---
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        messages.success(request, "Item added to cart.")
        return redirect('store:cart')
    return redirect('store:product_detail', product_id=product_id)


@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('store:cart')


@login_required
def cart(request):
    cart_items, total = get_cart_items(request)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


# --- UPDATE CART QUANTITY ---
@login_required
@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for key, value in request.POST.items():
            if key.startswith('quantities_'):
                product_id = key.replace('quantities_', '')
                try:
                    quantity = int(value)
                    if quantity > 0:
                        cart[product_id] = quantity
                    else:
                        cart.pop(product_id, None)
                except ValueError:
                    continue
        request.session['cart'] = cart
        messages.success(request, "Cart updated.")
    return redirect('store:cart')


# --- CHECKOUT ---
@login_required
def checkout(request):
    cart_items, total = get_cart_items(request)
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': total})


# --- PLACE ORDER ---
@login_required
def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('store:checkout')

        total = 0
        order = Order.objects.create(user=request.user, total_price=0)
        order_items = []

        for item_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=item_id)
                price = product.price
                subtotal = price * quantity
                total += subtotal

                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                order_items.append(order_item)
            except Product.DoesNotExist:
                continue

        order.total_price = total
        order.save()

        # Clear cart
        request.session['cart'] = {}

        # Email content
        items_text = "\n".join(
            [f"{item.product.name} (x{item.quantity}) - ₦{item.price * item.quantity}" for item in order_items]
        )
        message = f"""
Hi {request.user.username},

Thank you for your order #{order.id} on StyleVerse!

Order Summary:
{items_text}

Total: ₦{total}

We will notify you once your order is shipped.

– StyleVerse Team
"""
        send_mail(
            subject='StyleVerse Order Confirmation',
            message=f'Thank you for your order #{order.id}!. We are processing it.',
            from_email='styleverseinfo1@gmail.com',
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        return redirect('store:order_success')

    return redirect('store:checkout')


# --- ORDER SUCCESS ---
@login_required
def order_success(request):
    return render(request, 'store/order_success.html')


# --- ORDER TRACKING ---
@login_required
def order_tracking_view(request):
    tracking_updates= OrderTracking.objects.filter(
        order__user=request.user
    ).select_related('order').order_by('-updated_at')
    
    return render(request, 'store/order_tracking.html', {
        'tracking_updates':tracking_updates
    })


# --- ORDER HISTORY ---
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    reviewed_products = Review.objects.filter(user=request.user).values_list('product_id', flat=True)
    review_form = ReviewForm()

    context = {
        'page_obj': page_obj,
        'review_form': review_form,
        'reviewed_products': reviewed_products,
    }
    return render(request, 'store/order_history.html', context)


# --- SUBMIT REVIEW FROM ORDER HISTORY ---
@login_required
def submit_review_from_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Review submitted successfully.")
        else:
            messages.error(request, "Error submitting review.")

    return redirect('store:order_history')


# --- USER REVIEWS ---
@login_required
def user_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'store/user_reviews.html', {'reviews': reviews})


# --- ADD REVIEW (INLINE) ---
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    has_ordered = OrderItem.objects.filter(order__user=request.user, product=product).exists()
    if not has_ordered:
        return HttpResponseForbidden("You can only review products you have ordered.")

    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            Review.objects.create(product=product, user=request.user, comment=comment)
            return redirect('store:order_history')
    return redirect('store:product_detail', product_id=product.id)


# --- WISHLIST ---
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('store:product_detail', product_id=product.id)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    return redirect('store:wishlist_view')


@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    return render(request, 'store/wishlist.html', {'products': products})


# --- SEARCH ---
def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else []
    return render(request, 'store/search_results.html', {'products': products, 'query': query})



logger = logging.getLogger(__name__)

def send_tracking_update_email(tracking):
    """
    Sends an email to the user when an order tracking update is made.
    `tracking` should be an OrderTracking instance.
    """
    try:
        order = tracking.order
        user = order.user

        context = {
            'user': user,
            'order': order,
            'tracking': tracking,
        }

        subject = f"Your Order #{order.id} Has Been Updated"
        # Prefer DEFAULT_FROM_EMAIL, fallback to EMAIL_HOST_USER
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
        to_email = [user.email]

        text_content = f"Hi {user.username},\n\nYour order #{order.id} tracking status is now '{tracking.status}'."
        
        html_content = render_to_string('store/emails/tracking_update.html', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)  
    except Exception as exc:
        # Log error but don't crash admin
        logger.exception("Failed to send tracking update email for order %s: %s", getattr(tracking.order, 'id', 'unknown'), exc)