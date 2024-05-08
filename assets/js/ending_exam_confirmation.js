function confirmSubmission(slug, appName) {
    Swal.fire({
        title: 'پایان آزمون',
        text: "آیا از ثبت نهایی این آزمون اطمینان دارید؟",
        icon: 'question',
        showCancelButton: true,
        cancelButtonColor: '#d33',
        confirmButtonText: 'بله',
        cancelButtonText: 'خیر'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/course/${appName}/exam/${slug}/submit/final`;
        }
    });
    return false;
}