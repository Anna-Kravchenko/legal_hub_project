from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Avg
from .models import Service, Review, Client, Order, ServiceCategory
from .forms import OrderForm
import logging

logger = logging.getLogger('bureau')


def home_view(request):
    services = Service.objects.all()[:4]
    reviews = Review.objects.all()[:3]
    context = {
        'services': services,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)


def services_view(request):
    query = request.GET.get('q', '').strip()

    categories = ServiceCategory.objects.prefetch_related('services').all()

    if query:
        categories = [
            {
                "category": category,
                "services": category.services.filter(
                    is_active=True
                ).filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
                )
            }
            for category in categories
        ]

        categories = [
            item for item in categories
            if item["services"].exists()
        ]

    else:
        categories = [
            {
                "category": category,
                "services": category.services.filter(is_active=True)
            }
            for category in categories
        ]

    return render(request, "services.html", {
        "categories": categories,
        "query": query,
    })


from django.db.models import Avg

def reviews_view(request):
    reviews = Review.objects.filter(is_published=True)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'reviews.html', {
        'reviews': reviews,
        'average_rating': average_rating,
    })


def contacts_view(request):
    return render(request, 'contacts.html')


def order_view(request):
    # success_message = ""

    if request.method == "POST":
        logger.info("Order form submitted")
        form = OrderForm(request.POST, request.FILES)

        if form.is_valid():

            client, created = Client.objects.get_or_create(
                email=form.cleaned_data["email"],
                defaults={
                    "name": form.cleaned_data["client_name"],
                    "phone": form.cleaned_data["phone"],
                }
            )

            if created:
                logger.info("New client created: %s", client.email)
            else:
                logger.info("Existing client found: %s", client.email)
                client.name = form.cleaned_data["client_name"]
                client.phone = form.cleaned_data["phone"]
                client.save()
                logger.info("Client updated: %s", client.email)

            order = Order.objects.create(
                client=client,
                service=form.cleaned_data["service"],
                # source_language=form.cleaned_data["source_language"],
                # target_language=form.cleaned_data["target_language"],
                is_urgent=form.cleaned_data["is_urgent"],
                comment=form.cleaned_data["comment"],
                file=form.cleaned_data.get("file"),
                status="new",
            )
            logger.info("Order created: %s", order.id)
            # success_message = "Ваше замовлення успішно надіслано!"
            return redirect("order_success")
            # form = OrderForm()
    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'form': form,
        # 'success_message': success_message,
    })

def order_success(request):
    return render(request, "order_success.html")