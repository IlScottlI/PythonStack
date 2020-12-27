var code = 0;
var lang = '';
var userName = "";
var lists = [];
var plants = [];
var businesses = [];
var modules = [];
var departments = [];
var areas = [];
var statuses = [];
var types = [];
var reasons = [];
var selectedModules = [];
var selectedBusinesses = [];
var selectedDepartments = [];
var selectedAreas = [];
var userProfile = {};
var dayOfWeekNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
var selectedPlantId;
var selectedPlant;
var langs = [];
var langs_datePicker = [];
var langMenuItems = [];
var rules = []
if (window.location.pathname == '/request') {


    try {
        sessionStorage.removeItem('question_response')
        sessionStorage.removeItem('b_ids')
        sessionStorage.removeItem('m_ids')
        sessionStorage.removeItem('d_ids')
        sessionStorage.removeItem('a_ids')
        sessionStorage.removeItem('start_date')
        sessionStorage.removeItem('end_date')
        sessionStorage.removeItem('recurrenceRule')
        rules = []
    } catch (error) {

    }
}

function initlizeComboBoxes() {
    getFromStorage();
    initlizeBusinesses();
    initlizeModules();
    initlizeDepartments();
    initlizeAreas();
    initlizeType();
    initlizeReason();
    initlizeMaxRows();
    initlizeStatus();
    $('.viewFilter').on('change', () => {
        buildTable();
    })
    initlizeLanguage(localStorage.getItem('lang'));

}

// $('.approvals').html(`<span class="badge badge-light approvalCount">0</span>  Approvals`);
// $('.approvalCount').text(2);

$('.lang').on('click', (e) => {
    initlizeLanguage(e.target.id);
    window.location = ''
})


function initlizeLanguage(code) {
    localStorage.setItem('lang', code);
    $('.lang').removeClass("text-primary");
    DevExpress.localization.locale(code);
    DevExpress.localization.loadMessages({
        "en": {
            "appTitle": "Downtime Planner"
        },
        "de": {
            "appTitle": "Ausfallzeit Planer"
        },
        "ru": {
            "appTitle": "Планировщик простоев"
        }
    });
    $(".appTitle").text(DevExpress.localization.formatMessage("appTitle"));
    $("title").text(DevExpress.localization.formatMessage("appTitle"));
    $(`#${code}`).addClass("text-primary");
}

function getTerm(term) {
    let code = localStorage.getItem('lang')
    let translated
    langs.forEach((e) => {
        if (e.term == term & e.langCode == code) {
            translated = e.translated
        }
    })
    return translated
}
function getPickerTerm() {
    let locale
    let code = localStorage.getItem('lang')
    langs_datePicker.forEach((e) => {
        if (e.langCode == code) {
            locale = e
        }
    })
    return locale
}

function initlizeMaxRows() {
    $("#filter-maxRows").select2({
        language: lang,
        multiple: false,
        minimumResultsForSearch: Infinity
    });
}

function initlizeStatus() {
    try {
        $("#filter-status-1").select2({
            language: lang,
            data: statuses,
            multiple: true,
            maximumSelectionLength: 1
        });
    } catch (error) { }
}

function initlizeType() {
    try {
        $("#typeSelect").select2({
            language: lang,
        });
    } catch (error) { }
    try {
        $("#filter-type").select2({
            language: lang,
        });
    } catch (error) {

    }
}

function initlizeReason() {
    try {
        $("#reasonSelect").select2({
            language: lang,
        });
    } catch (error) { }
    try {
        $("#filter-reason").select2({
            language: lang,
        });
    } catch (error) { }
}

function initlizeBusinesses() {
    try {
        $("#buSelect").select2({
            language: lang,
            multiple: true,
        });
        $("#buSelect").on("change", function (e) {
            initlizeModules();
            initlizeDepartments();
            initlizeAreas();
        });
    } catch (error) { }
    try {
        $("#filter-business").select2({
            language: lang,
            multiple: true,
        });
        $("#filter-business").on("change", function (e) {
            initlizeModules();
            initlizeDepartments();
            initlizeAreas();
        });
    } catch (error) { }
}

function initlizeModules() {
    selectedModules = [];
    try {
        $("#moduleSelect").val(null).trigger("change");
    } catch (error) { }
    try {
        let array = $("#buSelect").select2("data");
        array.forEach((ele_a) => {
            modules.forEach((ele_b) => {
                if (ele_a.id == ele_b.buId) {
                    selectedModules.push(ele_b);
                }
            });
        });
        $("#moduleSelect").select2({
            language: lang,
            multiple: true,
        });
        $("#moduleSelect").on("change", function (e) {
            initlizeDepartments();
            initlizeAreas();
        });
    } catch (error) { }
    try {
        $("#filter-module").val(null).trigger("change");
    } catch (error) { }
    try {
        let array = $("#filter-business").select2("data");
        array.forEach((ele_a) => {
            modules.forEach((ele_b) => {
                if (ele_a.id == ele_b.buId) {
                    selectedModules.push(ele_b);
                }
            });
        });
        $("#filter-module").select2({
            language: lang,
            multiple: true,
        });
        $("#filter-module").on("change", function (e) {
            initlizeDepartments();
            initlizeAreas();
        });
    } catch (error) { }
}

function initlizeDepartments() {
    selectedDepartments = [];
    try {
        $("#deptSelect").val(null).trigger("change");
    } catch (error) { }
    try {

        $("#deptSelect").select2({
            language: lang,
            multiple: true,
        });
        $("#deptSelect").on("change", function (e) {
            initlizeAreas();
        });
    } catch (error) { }
    try {
        $("#deptSelect").val(null).trigger("change");
    } catch (error) { }
    try {
        $("#filter-department").select2({
            language: lang,
            multiple: true,
        });
        $("#filter-department").on("change", function (e) {
            initlizeAreas();
        });
    } catch (error) { }
}

function initlizeAreas() {
    selectedAreas = [];
    try {
        $("#areaSelect").val(null).trigger("change");
    } catch (error) { }
    try {
        $("#areaSelect").select2({
            language: lang,
            multiple: true,
        });
        $("#areaSelect").on("change", function (e) { });
    } catch (error) { }
    try {
        $("#filter-area").val(null).trigger("change");
    } catch (error) { }
    try {
        $("#filter-area").select2({
            language: lang,
            multiple: true,
        });
        $("#filter-area").on("change", function (e) { });
    } catch (error) { }
}

function alertToast(e, title, type, skipTimeout) {
    let color;
    switch (type) {
        case 'error':
            color = 'bg-danger'
            break;
        case 'success':
            color = 'bg-success'
            break;
        default:
            color = 'bg-info';
            break;
    }
    let id = Date.now();
    let item = `
    <div role="alert" class="toast ${color} fade show" id="${id}">
        <div class="toast-header">
            <strong class="mr-auto">${title}</strong><small>${type}</small>
            <button class="close ml-2 mb-1 close" onclick="remove(${id})">
                <span aria-hidden="true">×</span>
            </button>
        </div>
        <div role="alert" class="toast-body">
            <p>${e}</p>
        </div>
    </div>
`;
    if (!skipTimeout) {
        setTimeout(() => {
            remove(id);
        }, 5000);
    }


    $('#toastPanel').append(item);
    var toastPanel = setInterval(() => {
        $('#toastPanel').css({ display: "block" });
        if ($('#toastPanel').length < 1) {
            $('#toastPanel').css({ display: "none" });
            clearInterval(toastPanel);
        }
    }, 250);
}

function remove(id) {
    $(`#${id}`).remove();
}

function getFromStorage() {
    try {
        plants = JSON.parse(sessionStorage.getItem("plants"));
    } catch (e) {
        alertToast(e, 'Failed to load plants from SessionStorage', 'error');
    }
    try {
        statuses = JSON.parse(sessionStorage.getItem("statuses"));
    } catch (e) {
        alertToast(e, 'Failed to load statuses from SessionStorage', 'error');
    }
    try {
        types = JSON.parse(sessionStorage.getItem("types"));
    } catch (e) {
        alertToast(e, 'Failed to load types from SessionStorage', 'error');
    }
    try {
        reasons = JSON.parse(sessionStorage.getItem("reasons"));
    } catch (e) {
        alertToast(e, 'Failed to load reasons from SessionStorage', 'error');
    }
    try {
        businesses = JSON.parse(sessionStorage.getItem("businesses"));
    } catch (e) {
        alertToast(e, 'Failed to load businesses from SessionStorage', 'error');
    }
    try {
        modules = JSON.parse(sessionStorage.getItem("modules"));
    } catch (e) {
        alertToast(e, 'Failed to load modules from SessionStorage', 'error');
    }
    try {
        departments = JSON.parse(sessionStorage.getItem("departments"));
    } catch (e) {
        alertToast(e, 'Failed to load departments from SessionStorage', 'error');
    }
    try {
        areas = JSON.parse(sessionStorage.getItem("areas"));
    } catch (e) {
        alertToast(e, 'Failed to load areas from SessionStorage', 'error');
    }
}

