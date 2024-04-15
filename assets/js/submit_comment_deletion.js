function submit_deletion(id, app) {
    const deleteUrl = `/${app}/comment/delete/${id}#reply_section`;

    Swal.fire({
        title: 'حذف نظر',
        text: 'آیا از حذف این نظر اطمینان دارید؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'بله',
        cancelButtonText: 'نه'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = deleteUrl;
        }
    });
}