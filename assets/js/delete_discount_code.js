function deleteDiscountCode(formatted_total_price_with_discount) {
    divToHide = document.getElementById("discount-code-percent");
    divToHide.style.display = "none";

    finalPriceSpan = document.getElementById("total_price_with_discount");
    finalPriceSpan.innerText = formatted_total_price_with_discount;

    discount_input = document.getElementById("discountInput");
    discount_input.value = "";

    let submittedDiscount = document.getElementById("submittedDiscount")
    submittedDiscount.value = ""

}