function toggleFollowPrivateAccounts(following_id) {

    $.ajax({
        url: '/account/toggle/follow/private/accounts/',
        method: 'POST',
        data: {
            'following_id': following_id
        },
        success: function (response) {
            const button = document.getElementById("follow-btn");
            const svg = button.querySelector('svg');
            const pathElement = svg.querySelector('path');

            if (response.message === "requested") {
                button.classList.remove('bg-primary');
                button.classList.add('bg-success');
                button.querySelector('span').innerText = "درخواست داده شده";
                pathElement.setAttribute('d', 'M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z');
            }

            if (response.message === "unrequested") {
                button.classList.remove('bg-success');
                button.classList.add('bg-primary');
                button.querySelector('span').innerText = "فالو";
                pathElement.setAttribute('d', 'M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z');
            }

        },
    });
}
