function confirmToggleFollow(following_id) {
    Swal.fire({
        title: 'اطمینان از آن‌فالو کردن؟',
        text: 'این حساب کاربری شخصی است. اگر این حساب کاربری را آن‌فالو کنید، جهت فالو کردن مجدد باید درخواست بدهید.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'بله',
        cancelButtonText: 'نه'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/account/unfollow/private/accounts/',
                method: 'POST',
                data: {
                    'following_id': following_id
                },
                success: function (response) {
                    // Redirect to a new URL upon successful toggle
                    window.location.href = `${response.redirect_url}`;  // Replace with your desired redirect URL
                },
                error: function (xhr, status, error) {
                    console.error(error);
                    // Handle error if needed
                }
            });
        }
    });
}
