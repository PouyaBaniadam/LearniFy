function showVideoExamResult(slug) {
    $.ajax({
        type: 'GET',
        url: `/course/video/exam/${slug}/result`,
        dataType: 'json',
        success: function (response) {
            let examResults = response.exam_result;
            let content = '<table class="table" dir="ltr"><' +
                'thead>' +
                '<tr>' +
                '<th>تاریخ آزمون</th>' +
                '<th>درصد</th>' +
                '</tr>' +
                '</thead>' +
                '<tbody>';

            let counter = 1;

            for (let i = 0; i < examResults.length; i++) {
                let percentage = examResults[i]["percentage"];
                let resultStatus = examResults[i]["result_status"];
                let createdAt = examResults[i]["created_at"];
                let textColor = "black";

                switch (resultStatus) {
                    case "E":
                        textColor = "green";
                        break;
                    case "G":
                        textColor = "blue";
                        break;
                    case "N":
                        textColor = "black";
                        break;
                    case "B":
                        textColor = "red";
                        break;
                    default:
                        textColor = "orange";
                }

                content += '<tr>';
                content += '<td>' + createdAt + '</td>';
                content += '<td style="color: ' + textColor + '">' + percentage + '</td>';
                content += '<td>#' + counter + '</td>';
                content += '</tr>';

                counter++;
            }

            content += '</tbody></table>';

            Swal.fire({
                width: 500,
                title: 'نتایج آزمون',
                html: content,
                confirmButtonText: 'بستن',
            });
        },

        error: function (error) {
            Swal.fire({
                icon: 'error',
                title: 'خطا',
                text: error.responseJSON.error,
                confirmButtonText: 'باشه',
                confirmButtonColor: '#d33',
                timer: 3000
            });
        }
    });
}
