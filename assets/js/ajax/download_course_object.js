function downloadPDFCourse(slug, courseID) {
    const formData = {
        'course_id': courseID,
    };

    const form = $('<form>', {
        'action': `/course/pdf/${slug}/download/`,
        'method': 'POST',
        'target': '_blank'
    });

    $.each(formData, function (key, value) {
        form.append($('<input>', {
            'type': 'hidden',
            'name': key,
            'value': value
        }));
    });

    $('body').append(form);
    form.submit();
    window.close();
}
