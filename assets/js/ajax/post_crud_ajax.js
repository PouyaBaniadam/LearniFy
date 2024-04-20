
        function showPostDetail(imageUrl, postTitle, postCaption, postId) {
            Swal.fire({
                width: 550,
                title: postTitle,
                imageUrl: imageUrl,
                imageWidth: 500,
                imageHeight: 250,
                confirmButtonText: 'بستن',
                html: `
<div id="postDetailContainer">
    <p id="postCaption">${postCaption}</p>
    <button id="editButton" onclick="enableEditing(${postId})">✏️</button>
</div>
            `,
            });
        }

        function enableEditing(postId) {
            const postCaptionElement = document.getElementById('postCaption');
            const editButton = document.getElementById('editButton');

            const textarea = document.createElement('textarea');
            textarea.id = 'editedCaption';
            textarea.value = postCaptionElement.innerText;
            textarea.style.width = '100%';
            textarea.style.height = '100px';
            textarea.classList.add(
                'form-textarea',
                'w-full',
                '!ring-0',
                '!ring-offset-0',
                'bg-secondary',
                'border-0',
                'focus:border-border',
                'border-border',
                'rounded-xl',
                'text-sm',
                'text-foreground',
                'p-5'
            );
            postCaptionElement.replaceWith(textarea);
            editButton.innerHTML = `
        <button class="w-full h-11 inline-flex items-center justify-center gap-1 bg-success rounded-lg text-primary-foreground transition-all hover:opacity-80 px-4" onclick="saveChanges(${postId})">ذخیره</button>
    `;
        }

        function saveChanges(post_id) {
            const editedCaption = document.getElementById('editedCaption').value;
            const postId = post_id; // Replace with your post ID
            const data = {
                caption: editedCaption,
                post_id: postId
            };

            fetch(`/account/profile/post/caption/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Use a function to get CSRF token
                },
                body: JSON.stringify(data)
            })
                .then(response => {
                    if (response.ok) {
                        return response.json(); // Parse the response body as JSON
                    }
                })
                .then(data => {
                    // Update the UI with the new caption if successful
                    const postCaptionElement = document.createElement('p');
                    postCaptionElement.id = 'postCaption';
                    postCaptionElement.innerText = data.caption; // Access 'caption' property from response
                    const textarea = document.getElementById('editedCaption');
                    textarea.replaceWith(postCaptionElement);

                    // Reset the button to Edit mode
                    const editButton = document.getElementById('editButton');
                    editButton.innerHTML = '✏️';
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

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

        function showAddPostForm() {
            Swal.fire({
                icon: "info",
                title: 'افزودن پست',
                confirmButtonText: 'افزودن',
                html:
                    '<input id="imageInput" type="file" accept="image/*" required>' +
                    '<input id="titleInput" maxlength="50" type="text" class="form-textarea w-full form-textareaw-full !ring-0 !ring-offset-0 bg-secondary border-0 focus:border-border border-border rounded-xl text-sm text-foreground p-5!ring-0 mb-3 mt-3" placeholder="موضوع" required>' +
                    '<textarea id="captionInput" maxlength="1000" class="h-full form-textarea w-full form-textareaw-full !ring-0 !ring-offset-0 bg-secondary border-0 focus:border-border border-border rounded-xl text-sm text-foreground p-5!ring-0" placeholder="کپشن"></textarea>',
                focusConfirm: false,
                preConfirm: () => {
                    const imageInput = document.getElementById('imageInput');
                    const titleInput = document.getElementById('titleInput');
                    const captionInput = document.getElementById('captionInput');

                    if (!imageInput || !imageInput.files || !imageInput.files[0]) {
                        Swal.showValidationMessage('لطفاً یک تصویر انتخاب کنید');
                        return;
                    }

                    const formData = new FormData();
                    formData.append('image', imageInput.files[0]);
                    formData.append('title', titleInput.value);
                    formData.append('caption', captionInput.value);

                    return fetch('/account/profile/post/add/', {
                        method: 'POST',
                        body: formData,
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data && data.error) {
                                throw new Error(data.error);
                            } else {
                                Swal.fire({
                                    icon: 'success',
                                    title: 'پست با موفقیت افزوده شد.',
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

        document.addEventListener('DOMContentLoaded', function () {
            document.getElementById('deletePostBtn').addEventListener('click', function () {
                const postId = this.getAttribute('data-post-id');
                deletePost(postId);
            });
        });

        function deletePost(postId) {
            Swal.fire({
                title: 'اطمینان از حذف؟',
                text: 'این عملیات غیر قابل بازگشت است.',
                icon: 'warning',
                showCancelButton: true,
                cancelButtonColor: '#d33',
                confirmButtonText: 'بله',
                cancelButtonText: 'خیر'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch('/account/profile/post/delete/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': '{{ csrf_token }}'
                        },
                        body: JSON.stringify({postId: postId})
                    }).then(response => {
                        if (response.ok) {
                            Swal.fire({
                                title: 'حذف موفقیت آمیز',
                                text: 'پست شما با موفقیت حذف شد.',
                                icon: 'success',
                                confirmButtonText: 'باشه',
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    location.reload();
                                }
                            });
                        } else {
                            Swal.fire('Error!', 'Failed to delete post.', 'error');
                        }
                    }).catch(error => {
                        console.error('Error:', error);
                        Swal.fire('Error!', 'Failed to delete post.', 'error');
                    });
                }
            });
        }
