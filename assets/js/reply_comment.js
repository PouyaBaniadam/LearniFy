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

function setValue(id, name) {
    document.getElementById('cancel_reply_btn').style.display = "inline"
    document.getElementById('cancel_reply_to?').style.display = "inline"
    document.getElementById('parent_id').value = id;

    document.getElementById('reply_comment_id').innerText = name;

    const replySection = document.getElementById('reply_section');
    if (replySection) {
        replySection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function cancelReply() {
    // Disable further reply functionality
    document.getElementById('parent_id').value = '';
    document.getElementById('reply_comment_id').innerText = '';
    document.getElementById('cancel_reply_btn').style.display = 'none';
    document.getElementById('cancel_reply_to?').style.display = 'none';
}