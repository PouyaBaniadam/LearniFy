function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showAddDepositSlipReceiptForm() {
    Swal.fire({
        icon: "info",
        text: 'چنانچه مبلغ مذکور را کارت به کارت کردید، فیش واریزی را در این بخش آپلود کنید.',
        title: 'آپلود رسید خرید',
        confirmButtonText: 'آپلود',
        html: '<input id="imageInput" type="file" accept="image/*" required>',
        focusConfirm: false,
        preConfirm: () => {
            const imageInput = document.getElementById('imageInput');

            if (!imageInput || !imageInput.files || !imageInput.files[0]) {
                Swal.showValidationMessage('لطفاً یک تصویر انتخاب کنید');
                return;
            }

            const formData = new FormData();
            discount_code = document.getElementById("discountInput")
            formData.append('image', imageInput.files[0]);
            formData.append('discount_code', discount_code.value);

            return fetch('/cart/deposit/slip/add/', {
                    method: 'POST',
                    body: formData,
                }
            )
                .then(response => response.json())
                .then(data => {
                    if (data && data.error) {
                        throw new Error(data.error);
                    } else {
                        Swal.fire({
                            icon: 'success',
                            title: 'موفقیت',
                            text: 'فیش واریزی با موفقیت آپلود شد و بعد از تایید توسط تیم پشتیبانی، شما در دوره‌ها ثبت نام خواهید شد.',
                            confirmButtonText: 'باشه',
                        }).then(() => {
                            location.reload();
                        });
                    }
                })
                .catch(error => {
                    Swal.fire({
                        icon: 'error',
                        title: 'خطا در افزودن پست',
                        text: error.message || 'خطای ناشناخته رخ داده است',
                        confirmButtonText: 'باشه',
                        confirmButtonColor: 'red',
                    });
                });
        }
    });
}