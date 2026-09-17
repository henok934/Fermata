$(document).ready(function() {
    $('#bookingForm').on('submit', function(e) {
        e.preventDefault();

        const btn = $('#submitBtn');
        btn.prop('disabled', true).text('Processing Payment...');

        $.ajax({
            url: '/book/',  // views.py ላይ ወደተዘጋጀው telebirr_pay endpoint
            type: 'POST',
            data: {
                depcity: $('#depcity').val(),
                descity: $('#descity').val(),
                date: $('#journey_date').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                btn.prop('disabled', false).html('<i class="fas fa-wallet mr-1"></i> Pay with telebirr');

                if (response.status === 'SUCCESS' && response.toPayRequest) {
                    // telebirr In-App SDK Check
                    if (typeof telebirr !== 'undefined' && telebirr.pay) {
                        telebirr.pay({
                            toPayRequest: response.toPayRequest,
                            success: function(res) {
                                window.location.href = "/ticket/?outTradeNo=" + response.outTradeNo;
                            },
                            fail: function(err) {
                                alert("Payment Cancelled or Failed!");
                            }
                        });
                    } else {
                        alert("Order Created Successfully! Trade No: " + response.outTradeNo);
                    }
                } else {
                    alert(response.message || "Unable to initiate payment.");
                }
            },
            error: function() {
                btn.prop('disabled', false).html('<i class="fas fa-wallet mr-1"></i> Pay with telebirr');
                alert("Server error occurred. Please try again.");
            }
        });
    });
});
