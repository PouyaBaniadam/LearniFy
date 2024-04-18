function toggle_follow(followingId) {
    $.ajax({
        type: 'POST',
        url: '/account/toggle/follow/',
        data: {
            "following_id": followingId
        },
        success: function (response) {
            const button = document.getElementById("follow-btn");
            const svg = button.querySelector('svg');
            const pathElement = svg.querySelector('path');
            const followerCountSpan = document.getElementById("follower-count");

            if (response.message === "followed") {
                button.classList.remove('bg-primary');
                button.classList.add('bg-red-500');
                button.querySelector('span').innerText = "آن‌فالو";
                followerCountSpan.innerText = response.following_count
                pathElement.setAttribute('d', 'M22 10.5h-6m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM4 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 10.374 21c-2.331 0-4.512-.645-6.374-1.766Z');
            } else {
                button.classList.remove('bg-red-500');
                button.classList.add('bg-primary');
                button.querySelector('span').innerText = "فالو";
                pathElement.setAttribute('d', 'M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z');
                followerCountSpan.innerText = response.following_count
            }
        },
        error: function (xhr, status, error) {
            Swal.fire({
                icon: 'error',
                title: "فالو",
                text: xhr.responseJSON.message,
                confirmButtonText: 'باشه',
                confirmButtonColor: '#d33',
                timer: 3000
            });
        }
    });
}
