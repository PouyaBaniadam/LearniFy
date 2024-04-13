function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    // Follow button click
    $(document).on('click', '.follow-btn', function () {
        var username = $(this).data('username');
        followUser(username);
    });

    // Unfollow button click
    $(document).on('click', '.unfollow-btn', function () {
        var username = $(this).data('username');
        unfollowUser(username);
    });

    // Function to follow a user via AJAX
    function followUser(username) {
        const doc = document.getElementById("follower-count");
        doc.innerText = Number(doc.innerText) + 1;
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: `/account/follow/${username}/`,
            headers: {'X-CSRFToken': csrftoken},
            success: function (response) {
                //Swal.fire({
                //    icon: 'success',
                //    title: 'فالو',
                //    text: response.message,
                //    confirmButtonText: 'باشه',
                //    timer: 3000
                //});
                // Change button to Unfollow style
                $('.follow-btn[data-username="' + username + '"]')
                    .removeClass('follow-btn')
                    .addClass('unfollow-btn')
                    .removeClass('bg-primary') // Remove current background color class
                    .addClass('bg-red-500')   // Add new background color class
                    .html('<span class="font-semibold text-sm">آن‌فالو</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"></path></svg>');
            },
            error: function (xhr, status, error) {
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.error : "An error occurred";
                Swal.fire({
                    icon: 'error', title: 'فالو', text: errorMessage, confirmButtonText: 'OK'
                });
            }
        });
    }

    // Function to unfollow a user via AJAX
    function unfollowUser(username) {
        const doc = document.getElementById("follower-count");
        doc.innerText = Number(doc.innerText) - 1;
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: `/account/unfollow/${username}/`,
            headers: {'X-CSRFToken': csrftoken},
            success: function (response) {
                //Swal.fire({
                //  icon: 'warning',
                //title: 'آن‌فالو',
                //text: response.message,
                //confirmButtonText: 'باشه',
                //timer: 3000
                //});
                // Change button to Follow style
                $('.unfollow-btn[data-username="' + username + '"]')
                    .removeClass('unfollow-btn')
                    .addClass('follow-btn')
                    .removeClass('bg-red-500')   // Remove current background color class
                    .addClass('bg-primary')      // Add new background color class
                    .html('<span class="font-semibold text-sm">فالو</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"></path></svg>');
            },
            error: function (xhr, status, error) {
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.error : "مشکلی پیش آمده!";
                Swal.fire({
                    icon: 'error', title: 'آن‌فالو', text: errorMessage, confirmButtonText: 'OK'
                });
            }
        });
    }
});

