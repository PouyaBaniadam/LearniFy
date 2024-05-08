document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('pdf_exam_link').addEventListener('click', function (e) {
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
                window.location.href = this.getAttribute('data-url');
            }
        });
    });
});