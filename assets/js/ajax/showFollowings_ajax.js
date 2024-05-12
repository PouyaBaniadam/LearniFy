function showFollowings(user, owner) {
    var formData = {
        'user': user,
        'owner': owner,
    };

    $.ajax({
        type: 'POST',
        url: '/account/followings/list/',
        data: formData,
        dataType: 'json',
        success: function (response) {
            let followingsHtml = '<ul style="text-align: left;">';

            response.followings.forEach(function(following) {
                followingsHtml += `<a href="/account/profile/${following[0]}">
                    <li dir="ltr" style="display: flex; align-items: center;" class="mt-3">
                    <div class="flex-shrink-0 w-10 h-10 rounded-full overflow-hidden mr-2">
                    <img src="${following[1]}" class="w-full h-full object-cover"
                         alt="تصویر پروفایل"/>
                    </div>
                    <p style="margin-left: 20px">${following[0]}</p>
                    <p style="margin-left: 20px">${following[2]}</p>
                    <span class="flex items-center justify-center w-12 h-12 bg-background rounded-full text-yellow-500">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                    class="w-5 h-5">
                    <path fill-rule="evenodd"
                    d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401Z"
                    clip-rule="evenodd"></path>
                    </svg>
                    </span>
                    </li>
                    </a>`;
            });
            followingsHtml += '</ul>';

            Swal.fire({
                title: 'فالویینگ‌‌ها',
                html: followingsHtml,
                confirmButtonText: 'بستن',
            });
        },
        error: function (error) {
            Swal.fire({
                icon: 'error',
                title: 'خطا',
                text: error.responseJSON.error,
                confirmButtonText: 'باشه',
                confirmButtonColor: '#d33',
            });
        }
    });
}
