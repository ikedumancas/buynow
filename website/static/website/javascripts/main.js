function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}

function isValidCardNumber(cardNumber) {
  var card_length = cardNumber.length;
  if((card_length < 12) || (card_length > 19)){
    return false;
  }
  return true;
}

function isValidExpiration(month, year){
  curr_date = new Date();
  curr_month = curr_date.getMonth()+1;
  curr_year = curr_date.getFullYear();
  if( year >= curr_year ) {
    if((curr_year == year))
    if((year == curr_year) && (month < curr_month)){
      return false;
    }else{
      return true;
    }
  }else{
    return false;
  }
}

function isValidCode (code) {
  var code_length = code.length;
  if((code_length < 3) || (code_length > 4)){
    return false;
  }
  return true;
}

function checkPayPalLoggedIn() {
  display = $('#braintree-paypal-loggedout').css('display'); // return none if paypal logged in
  $('#credit-card-inputs').css('display', display);
}

function new_payment(){
  console.log('creating post'); // sanity check
  $.ajax({
    url: 'ajax_pay/',
    type: 'POST',
    data: {
      email: $('#email').val(),
      payment_method_nonce: $('input[name=payment_method_nonce]').val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success : function(json) {
      console.log(json);
      if(json.status=='error'){
        if(!$('#errorsListContainer').length > 0){
          $('#paymentFormModal .modal-body').prepend('<div class="alert alert-danger" role="alert" id="errorsListContainer"></div>');
        }
        $('#errorsListContainer').html('<ul></ul>');
        // display form errors
        if(json.errors.form){
          for(var k in json.errors.form){
            for(x in json.errors.form[k]){
              $('#errorsListContainer ul').append("<li>" + k.toUpperCase() + ": " + json.errors.form[k][x] + "</ul>");
            }
          }
        // display braintree errors
        }else if(json.errors.braintree){
          for(x in json.errors.braintree){
            $('#errorsListContainer ul').append("<li>" + json.errors.braintree[x] + "</ul>");
          }
        }
      }else{
        window.location = "thanks/";
      }
    },
    error: function(xhr,errmsg,err){
      console.log(err);
      console.log(errmsg);
      console.log(xhr);
    }
  });
}

$(function() {
  var client = new braintree.api.Client({clientToken: clientToken});

  braintree.setup(clientToken, "custom", {
    id: "paymentForm",
    paypal: {
      container: "paypal-container",
      singleUse: true,
      amount: 29.99,
      currency: "USD",
    }
  });


  // Custom Validation on payment
  $('#submitPayment').click(function(event) {
    event.preventDefault();
    var error_count = 0;
    var email = $('#email');
    var card_no = $('#cardNumber');
    var code = $('#cardcv');
    var expire_month = $('#expire_month');
    var expire_year = $('#expire_year');
    
    if(!isEmail(email.val())){
      email.parent('.form-group').addClass('has-error');
      error_count++;
    }
    
    if($('#credit-card-inputs').css('display')=='block'){
      if(!isValidCardNumber(card_no.val())){
        card_no.parent('.form-group').addClass('has-error');
        error_count++; 
      }
      if(!isValidCode(code.val())){
        code.parent('.form-group').addClass('has-error');
        error_count++; 
      }
      if(!isValidExpiration(expire_month.val(), expire_year.val())){
        expire_month.parent('.form-group').addClass('has-error');
        expire_year.parent('.form-group').addClass('has-error');
        error_count++;
      }

      if(error_count==0){
        client.tokenizeCard({
          number: card_no.val(),
          expirationMonth: "12",
          expirationYear: "12",
          cvv: code.val()
        }, function (err, nonce) {
          console.log(err);
          $('input[name=payment_method_nonce]').val(nonce);
          new_payment();
        });
      }
    }else{
      if(error_count==0){
        new_payment();
      }
    }
  });
  window.setInterval(checkPayPalLoggedIn, 500);
});