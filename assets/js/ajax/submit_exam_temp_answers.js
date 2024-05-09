function sendData(question, selectedAnswer, slug, appName) {
    $.ajax({
        url: `/course/${appName}/exam/${slug}/submit/temp/`,
        method: 'POST',
        data: {
            'question': question,
            'selected_answer': selectedAnswer
        },
        success: function (response) {
            let question_id;
            if (response.message === "removed") {
                let question_id = response.id;
                input = document.getElementById(question_id);
                input.checked = false;
            }
        },
        error: function (xhr, status, error) {
            console.log("Error");
        }
    });
}
