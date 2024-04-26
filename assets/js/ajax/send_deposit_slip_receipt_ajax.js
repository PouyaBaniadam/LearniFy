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

function showAddDepositSlipReceiptForm(cardNumber, ownerName, type, redirectUrl) {
    if (type === "BUY") {
        Swal.fire({
            icon: "info",
            title: 'آپلود فیش واریزی',
            confirmButtonText: 'آپلود',
            html: `<p>چنانچه مبلغ مذکور را به شماره کارت <span class="text-primary">${cardNumber}</span> (به نام <span class="text-primary">${ownerName}</span>) کارت به کارت کردید، فیش واریزی را در این بخش آپلود کنید.</p>` +
                '<br>' +
                '<input id="imageInput" type="file" accept="image/*" required>',
            focusConfirm: false,
            preConfirm: () => {
                const imageInput = document.getElementById('imageInput');

                if (!imageInput || !imageInput.files || !imageInput.files[0]) {
                    Swal.showValidationMessage('لطفاً یک تصویر انتخاب کنید');
                    return;
                }

                const formData = new FormData();
                let discount_code = document.getElementById("submittedDiscount")
                formData.append('image', imageInput.files[0]);
                formData.append('discount_code', discount_code.value);

                return fetch('/financial/deposit/slip/add/', {
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
                                text: data.message,
                                confirmButtonText: 'باشه',
                            }).then(() => {
                                location.reload();
                            });
                        }
                    })
                    .catch(error => {
                        discountInput = document.getElementById("discountInput");
                        discountInput.value = "";

                        Swal.fire({
                            icon: 'error',
                            title: 'خطا در آپلود فیش واریزی',
                            text: error.message || 'خطای ناشناخته رخ داده است',
                            confirmButtonText: 'باشه',
                            confirmButtonColor: '#d33',
                            timer: 3000
                        });
                    });
            }
        });
    } else {
        Swal.fire({
            icon: "info",
            title: 'آپلود فیش واریزی',
            confirmButtonText: 'آپلود',
            html: `<p>چنانچه مبلغ مذکور را به شماره کارت <span class="text-primary">${cardNumber}</span> (به نام <span class="text-primary">${ownerName}</span>) کارت به کارت کردید، فیش واریزی را در این بخش آپلود کنید.</p>` +
                '<br>' +
                '<input id="imageInput" type="file" accept="image/*" required>',
            focusConfirm: false,
            preConfirm: () => {
                const imageInput = document.getElementById('imageInput');

                if (!imageInput || !imageInput.files || !imageInput.files[0]) {
                    Swal.showValidationMessage('لطفاً یک تصویر انتخاب کنید');
                    return;
                }

                const formData = new FormData();
                formData.append('image', imageInput.files[0]);

                return fetch('/account/wallet/charge/', {
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
                                text: data.message,
                                confirmButtonText: 'باشه',
                            }).then(() => {
                                window.location.href = redirectUrl;
                            });
                        }
                    })
                    .catch(error => {
                        Swal.fire({
                            icon: 'error',
                            title: 'خطا در آپلود فیش واریزی',
                            text: error.message || 'خطای ناشناخته رخ داده است',
                            confirmButtonText: 'باشه',
                            confirmButtonColor: '#d33',
                            timer: 3000
                        });
                    });
            }
        });
    }
}