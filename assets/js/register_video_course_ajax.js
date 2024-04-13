function register_video_course(courseId) {
    console.log(courseId)
    $.ajax({
        type: 'POST',
        url: `/course/video/register/`,
        data: {
            "courseId": courseId
        },
        success: function (response) {

            Swal.fire({
                icon: 'success',
                title: "ثبت نام در دوره",
                text: response.message,
                confirmButtonText: 'باشه',
                timer: 3000
            });
        },
        error: function (xhr, status, error) {
            Swal.fire({
                icon: 'error',
                title: "ثبت نام در دوره",
                text: xhr.responseJSON.message,
                confirmButtonText: 'باشه',
                confirmButtonColor: '#d33',
                timer: 3000
            });
        }
    });
}