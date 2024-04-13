document.addEventListener('DOMContentLoaded', function () {
    const logoutButtons = document.querySelectorAll('.logout-button');

    if (logoutButtons) {
        logoutButtons.forEach(function (button) {
            button.addEventListener('click', function (e) {
                e.preventDefault();

                Swal.fire({
                    title: 'خروج از حساب',
                    text: 'آیا از خروج خود اطمینان دارید؟',
                    icon: 'warning',
                    showCancelButton: true,
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'بله',
                    cancelButtonText: 'خیر'
                }).then((result) => {
                    if (result.isConfirmed) {
                        const logoutUrl = button.parentElement.getAttribute('href');
                        if (logoutUrl) {
                            window.location.href = logoutUrl;
                        }
                    }
                });
            });
        });
    }
});
