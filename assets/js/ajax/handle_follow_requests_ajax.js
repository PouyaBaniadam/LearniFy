function handleFollowRequests(follower, following, mode) {
    var data = {
        follower: follower,
        following: following,
        mode: mode,
    };

    $.ajax({
        type: "POST",
        url: "/account/handle/follow/requests/",
        data: data,
        dataType: "json",
        success: function (response) {
            if (response.message === "accepted") {
                const button_divs = document.getElementById("followRequestButtons");
                const title_div = document.getElementById("follow-title");
                const message_div = document.getElementById("follow-message");

                button_divs.style.display = "none";
                title_div.innerText = "فالو";

                // Function to strip HTML tags from a string
                function stripHtmlTags(html) {
                    const doc = new DOMParser().parseFromString(html, 'text/html');
                    return doc.body.textContent || "";
                }

                // Set the innerText of message_div after stripping HTML tags
                message_div.innerText = stripHtmlTags(response.message_text);

            }
            if (response.message === "rejected") {
                const whole_div = document.getElementById("whole-rejection-div");

                whole_div.style.display = "none"

            }
        },
    });
}
