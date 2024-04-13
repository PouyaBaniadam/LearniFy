$(document).ready(function () {
    $('.add-to-favorites-btn').click(function (e) {
        e.preventDefault();
        var button = $(this);
        var examId = button.data('exam-id');
        console.log(examId)
        $.ajax({
            type: 'POST',
            url: '/course/exam/favorite/toggle/',
            data: {
                'exam_id': examId,
            },
            success: function (data) {
                if (data.success) {
                    if (data.action === 'added') {
                        button.removeClass('text-muted bg-secondary hover:text-red-500')
                            .addClass('text-red-500');
                    } else if (data.action === 'removed') {
                        // Exam was removed from favorites
                        button.removeClass('text-red-500 bg-yellow-200')
                            .addClass('text-muted bg-secondary hover:text-red-500');
                    }
                } else {
                    console.log('Failed to toggle favorite.');
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const loginFirstButtons = document.querySelectorAll('.login-first');

    loginFirstButtons.forEach(button => {
        button.addEventListener('click', function () {
            Swal.fire({
                icon: 'warning',
                title: 'اهراز هویت',
                text: 'جهت افزودن این آزمون به لیست علاقه‌مندی‌های خود، ابتدا وارد حساب کاربری خود شوید.',
                confirmButtonText: 'باشه',
                // TODO: Change the host name for footer
                footer: '<a href="http://127.0.0.1:8000/account/login">ورود به حساب کاربری</a>'
            });
        });
    });
});