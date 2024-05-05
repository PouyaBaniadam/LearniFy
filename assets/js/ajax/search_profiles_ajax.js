$(document).ready(function () {
    $('#search-profile-input').on('input', function () {
        var query = $(this).val();
        if (query.length >= 3) {
            $.ajax({
                url: '/account/search/',
                method: 'GET',
                data: {query: query},
                success: function (response) {
                    var searchResults = $('#search-profile-results');
                    searchResults.empty();

                    var resultsContainer = $('<div>').addClass('search-profile-results-container');
                    if (response.results.length > 0) {
                        response.results.forEach(function (result) {
                            var profileLink = $('<a>').attr('href', '/account/profile/' + result.slug).text(result.username);
                            var listItem = $('<div>').addClass('result-item').append(profileLink);
                            resultsContainer.append(listItem);
                        });
                    } else {
                        resultsContainer.append('<p class="font-bold text-red-500">هیچ نتیجه‌‌ای برای جست‌‌جوی شما یافت نشد!</p>');
                    }

                    searchResults.append(resultsContainer);
                },

                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        } else {
            $('#search-profile-results').html('');
        }
    });
});
