$(document).ready(function () {
    $('button[type="submit"]').click(function (event) {
        event.preventDefault();

        var discountCode = $('#discountInput').val();

        var formData = {
            'discount_code': discountCode
        };

        $.ajax({
            type: 'POST',
            url: '/cart/discount/apply/',
            data: formData,
            dataType: 'json',
            success: function (response) {
                var span = document.getElementById("total_price_with_discount");
                span.innerText = response.final_price;

                $('.flex.items-center.justify-between.gap-3').show();

                var discountDiv = document.getElementById("discount-code-percent");
                discountDiv.style.display = "flex";

                var discountValueSpan = discountDiv.querySelector(".font-black.text-base.text-success.text-foreground");
                discountValueSpan.innerText = response.discount_percent;

                Swal.fire({
                    icon: 'success',
                    title: 'موفقیت',
                    text: response.message,
                    confirmButtonText: 'باشه',
                    timer:3000
                });
            },
            error: function (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'خطا',
                    text: error.responseJSON.message,
                    confirmButtonText: 'باشه',
                    confirmButtonColor: '#d33',
                    timer:3000
                });
            }
        });
    });
});