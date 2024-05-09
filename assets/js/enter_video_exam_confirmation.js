document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.video_exam_link_button');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            Swal.fire({
                title: 'ورود به آزمون',
                text: "آیا از ورود به آزمون اطمینان دارید؟ بعد از تایید، امکان ورود تا 24 ساعت آینده وجود نخواهد داشت.",
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'بله',
                cancelButtonText: 'خیر'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = button.getAttribute('data-url');
                }
            });
        });
    });
});
