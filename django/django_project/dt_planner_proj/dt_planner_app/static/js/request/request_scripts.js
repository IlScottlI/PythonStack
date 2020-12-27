$(document).ready(function () {
    getLanguage()
    initilizeRepeat();
    $('#downtimeOwner').select2()
    initilizeDatePickers();
    initlizeComboBoxes();
    $('#buSelect').val(0).trigger('change');

});
