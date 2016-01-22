import braintree
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)


def index(request):
    context = {}
    errors = []
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            cvv = form.cleaned_data['cvcode']
            expirem = form.cleaned_data['expirem']
            expirey = form.cleaned_data['expirey']
            cardnumber = form.cleaned_data['cardnumber']
            expire_date = '%s/%s' % (expirem, expirey)
            price = '29.99'
            payment = braintree.transaction.Transaction.sale({
                "amount": price,
                "credit_card": {
                    "number": cardnumber,
                    "expiration_date": expire_date,
                    "cvv": cvv
                },
                "customer": {
                    "email": email,
                }
            })
            if payment.is_success:
                order = Order(
                    email=email,
                    transaction_id=payment.transaction.id,
                    cvcode=cvv,
                    expirem=expirem,
                    expirey=expirey,
                    cardnumber=cardnumber,
                    price=Decimal(price)
                )
                order.save()
                request.session['email'] = email
                return redirect('thanks')
            else:
                for error in payment.errors.deep_errors:
                    errors.append(error.message)

        context = {'errors': errors, 'form': form}

    return render(request, 'website/index.html', context)


def thanks(request):
    context = {'email': request.session['email']}
    return render(request, 'website/thanks.html', context)
