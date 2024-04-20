function register_course(courseId, appName) {
    Swal.fire({
        title: 'ثبت نام',
        text: 'آیا از ثبت نام در دوره اطمینان دارید؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'خیر',
        cancelButtonColor: '#d33'

    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: 'POST',
                url: `/${appName}/video/register/`,
                data: {
                    "courseId": courseId
                },
                success: function (response) {
                    Swal.fire({
                        icon: 'success',
                        title: 'ثبت نام در دوره',
                        text: response.message,
                        confirmButtonText: 'باشه',
                        timer: 3000
                    });
                },
                error: function (xhr, status, error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'ثبت نام در دوره',
                        text: xhr.responseJSON.message,
                        confirmButtonText: 'باشه',
                        confirmButtonColor: '#d33',
                        timer: 3000
                    });
                }
            });
        }
    });
}
