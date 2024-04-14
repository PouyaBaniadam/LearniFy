function toggleCart(courseId, courseType) {
    var data = {
        course_type: courseType,
        course_id: courseId,
    };

    $.ajax({
        type: "POST",
        url: "/cart/toggle/",  // Update this URL to your Django endpoint
        data: data,
        dataType: "json",  // Assuming the backend returns JSON
        success: function (response) {
            // Select all elements with class 'cart-text'
            var spans = document.querySelectorAll('.cart-text');

            spans.forEach(function (span) {
                if (response.message === "added") {
                    // Update text when item is added
                    span.innerText = "افزودن به سبد خرید";
                } else if (response.message === "removed") {
                    // Update text when item is removed
                    span.innerText = "حذف از سبد خرید";
                }
            });

            cart_items_count = document.getElementById("cart-items-count");
            cart_items_count.innerText = response.cart_items_count;
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error toggling cart:", errorThrown);
        }
    });
}
