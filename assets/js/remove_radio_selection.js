    function clearRadioSelection(section) {
        const radioButtons = document.getElementsByName(section);
        radioButtons.forEach(function (radio) {
            radio.checked = false;
        });

        event.preventDefault();
        return false;
    }