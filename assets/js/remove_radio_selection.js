    function clearRadioSelection(section) {
        var radioButtons = document.getElementsByName(section);
        radioButtons.forEach(function (radio) {
            radio.checked = false;
        });

        // Prevent form submission
        event.preventDefault();
        return false;
    }