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
                footer: '<a href="https://learnifyacademy2000.pythonanywhere.com/account/login">ورود به حساب کاربری</a>'
            });
        });
    });
});