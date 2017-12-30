from django.shortcuts import render


def payment_view(request):
    if request.method == 'POST':
        restaurant = request.POST.get('restaurant')
        information = request.POST.get('information')
        name = request.POST.get('name')
        party = request.POST.get('party')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        context = {
            'restaurant': restaurant,
            'information': information,
            'name': name,
            'party': party,
            'phone_number': phone_number,
            'email': email,
        }
        return render(request, 'reservation/payment.html', context)
