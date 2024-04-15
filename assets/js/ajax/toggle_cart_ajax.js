function toggleCart(courseId, courseType) {
    const data = {
        course_type: courseType,
        course_id: courseId,
    };

    $.ajax({
        type: "POST",
        url: "/cart/toggle/",
        data: data,
        dataType: "json",
        success: function (response) {
            const spans = document.querySelectorAll('.cart-text');
            const button = document.getElementById("main-cart-btn");

            if (response.message === "added") {
                button.classList.remove('bg-red-500');
                button.classList.add('bg-primary')
            } else if (response.message === "removed") {
                button.classList.remove('bg-primary');
                button.classList.add('bg-red-500');
            }

            spans.forEach(function (span) {
                if (response.message === "added") {
                    span.innerText = "افزودن به سبد خرید";

                } else if (response.message === "removed") {
                    // Update text when item is removed
                    span.innerText = "حذف از سبد خرید";
                }
            });

            let cart_items_count = document.getElementById("cart-items-count");
            cart_items_count.innerText = response.cart_items_count;
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error toggling cart:", errorThrown);
        }
    });
}
