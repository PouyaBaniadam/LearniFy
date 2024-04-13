document.addEventListener("DOMContentLoaded", function () {
    const loginFirstButtons = document.querySelectorAll('.login-first');

    loginFirstButtons.forEach(button => {
        button.addEventListener('click', function () {
            Swal.fire({
                icon: 'warning',
                title: 'اهراز هویت',
                text: 'ابتدا وارد حساب کاربری خود شوید.',
                confirmButtonText: 'باشه',
                // TODO: Change the host name for footer
                footer: '<a href="http://127.0.0.1:8000/account/login">ورود به حساب کاربری</a>'
            });
        });
    });
});