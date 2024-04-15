$(document).ready(function () {
    $('#newsletterForm').submit(function (event) {
        event.preventDefault();

        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function (response) {

                Swal.fire({
                    icon: 'success',
                    title: 'ثبت نام در خبرنامه',
                    text: response.message,
                    confirmButtonText: 'باشه',
                    timer: 3000
                });
            },
            error: function (xhr, status, error) {

                Swal.fire({
                    icon: 'error',
                    title: 'ثبت نام در خبرنامه',
                    text: xhr.responseJSON.message,
                    confirmButtonText: 'باشه',
                    confirmButtonColor: '#d33',
                    timer: 3000
                });
            }
        });
    });
});
