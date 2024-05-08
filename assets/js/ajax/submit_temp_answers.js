function sendData(question, selectedAnswer, slug, appName) {
    $.ajax({
        url: `/course/${appName}/exam/${slug}/submit/temp/`,
        method: 'POST',
        data: {
            'question': question,
            'selected_answer': selectedAnswer
        },
        success: function (response) {
            console.log("Success");
        },
        error: function (xhr, status, error) {
            // Handle error response if needed
        }
    });
}