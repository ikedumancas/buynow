import braintree
from datetime import date
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
    bt_token = braintree.ClientToken.generate()
    curr_year = date.today().year
    expire_months = range(1, 13)
    expire_years = range(curr_year, curr_year + 11)
    context = {
        'bt_token': bt_token,
        'expire_months': expire_months,
        'expire_years': expire_years
    }
    errors = []
    if request.method == 'POST':
        nonce = request.POST["payment_method_nonce"]
        form = OrderForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            price = '29.99'
            payment = braintree.Transaction.sale({
                "amount": price,
                "payment_method_nonce": nonce
            })
            if payment.is_success:
                order = Order(
                    email=email,
                    transaction_id=payment.transaction.id,
                    price=Decimal(price),
                    card_type=payment.transaction.credit_card['card_type'],
                    last_4=payment.transaction.credit_card['last_4']
                )
                order.save()
                request.session['email'] = email
                return redirect('thanks')
            else:
                for error in payment.errors.deep_errors:
                    errors.append(error.message)

        context = {
            'bt_token': bt_token,
            'expire_months': expire_months,
            'expire_years': expire_years,
            'errors': errors,
            'form': form
        }

    return render(request, 'website/index.html', context)


def thanks(request):
    context = {'email': request.session['email']}
    return render(request, 'website/thanks.html', context)
