$(function() {
  
  function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
  }
  
  function isValidCardNumber (cardNumber) {
    var card_length = cardNumber.length;
    if((card_length < 12) || (card_length > 19)){
      return false;
    }
  }

  function isValidCode (code) {
    var code_length = code.length;
    if((code_length < 3) || (code_length > 4)){
      return false;
    } 
  }

  braintree.setup(clientToken, "custom", {
    id: "paymentForm",
    onReady: function (integration) {
      checkout = integration;
    },
    paypal: {
      container: "paypal-container",
      singleUse: true,
      amount: 29.99,
      currency: "USD",
    },
    onSuccess: function(){
      alert(1);
    },
    onPaymentMethodReceived: function (obj) {
      console.log(obj);
      var error_count = 0;
      if(obj.type=="CreditCard"){
        var email = $('#email');
        var card_no = $('#cardNumber');
        var code = $('#cardcv');

        if(!isEmail(email.val())){
          email.parent('.form-group').addClass('has-error');
          error_count++;
        }
        if(!isValidCardNumber(card_no.val())){
          card_no.parent('.form-group').addClass('has-error');
          error_count++; 
        }
        if(!isValidCode(code.val())){
          code.parent('.form-group').addClass('has-error');
          error_count++; 
        }
      }
      if(error_count==0){
        $('#paymentForm').append('<input type="hidden" name="payment_method_nonce" value="'+obj.nonce+'" />');
        $('#paymentForm').submit();
      }
    }
  });
});