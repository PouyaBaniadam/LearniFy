function toggle_account_status() {
    $.ajax({
        type: 'POST',
        url: '/account/toggle/account/status/',
        data: {},
        success: function (response) {
            const button = document.getElementById("change-account-status-btn");
            const svg = button.querySelector('svg');
            const pathElement = svg.querySelector('path');

            if (response.account_status === "private") {
                button.classList.remove('bg-primary');
                button.classList.add('bg-red-500');
                button.querySelector('span').innerText = "شخصی";
                pathElement.setAttribute('d', 'M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z');
            } else {
                button.classList.remove('bg-red-500');
                button.classList.add('bg-primary');
                button.querySelector('span').innerText = "عمومی";
                // Update the SVG path data
                pathElement.setAttribute('d', 'M13.5 10.5V6.75a4.5 4.5 0 1 1 9 0v3.75M3.75 21.75h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H3.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z');
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
