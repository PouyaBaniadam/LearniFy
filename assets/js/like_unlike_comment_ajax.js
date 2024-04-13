function toggleLike(commentId, app) {
    const likeBtn = document.getElementById(`likeBtn-${commentId}`);
    const likeCountElement = document.getElementById(`likeCount-${commentId}`); // Assuming you have an element for displaying like count
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/${app}/like_comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({comment_id: commentId})
    })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                likeBtn.classList.add('text-red-500');
                // Increase like count by 1 if the comment was liked
                if (likeCountElement) {
                    likeCountElement.textContent = parseInt(likeCountElement.textContent) + 1;
                }
            } else {
                likeBtn.classList.remove('text-red-500');
                // Decrease like count by 1 if the comment was unliked
                if (likeCountElement && parseInt(likeCountElement.textContent) > 0) {
                    likeCountElement.textContent = parseInt(likeCountElement.textContent) - 1;
                }
            }
        })
        .catch(error => console.error('Error:', error));
}
