from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Avg
from .models import Service, Review, Client, Order
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

    services = Service.objects.filter(is_active=True)

    if query:
        services = services.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'services.html', {
        'services': services,
        'query': query,
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
        form = OrderForm(request.POST)

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
                source_language=form.cleaned_data["source_language"],
                target_language=form.cleaned_data["target_language"],
                comment=form.cleaned_data["comment"],
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