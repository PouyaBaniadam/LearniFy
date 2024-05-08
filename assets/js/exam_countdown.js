const countdownElement = document.getElementById('countdown');

function startCountdown(durationInSeconds, slug) {
    let remainingTime = durationInSeconds;

    const intervalId = setInterval(() => {
        remainingTime--;

        const hours = Math.floor(remainingTime / 3600);
        const minutes = Math.floor((remainingTime % 3600) / 60);
        const seconds = remainingTime % 60;
        countdownElement.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        if (remainingTime <= 0) {
            clearInterval(intervalId);
            window.location.href = `/course/pdf/exam/${slug}/submit/final`;
        }
    }, 1000);
}
