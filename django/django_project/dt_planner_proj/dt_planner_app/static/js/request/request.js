var langs = [];

var question_ids = [];
var approver_ids = [];
var approver_ids_ = [];
var contributor_ids = [];
var contributor_ids_ = [];
var questionBank = []
var approverBank = []
var contributorBank = []




function initilizeDatePickers(start, end, repeatEnd) {
    if (start) {
        let loopstart = setInterval(() => {
            try {
                if (window.location.pathname == '/request') {
                    $("#form-eventStart").daterangepicker({
                        timePicker: true,
                        singleDatePicker: true,
                        showDropdowns: true,
                        timePicker24Hour: true,
                        locale: getPickerTerm().locale,
                        startDate: moment(start),
                    });
                    $("#form-eventEnd").daterangepicker({
                        timePicker: true,
                        singleDatePicker: true,
                        showDropdowns: true,
                        timePicker24Hour: true,
                        locale: getPickerTerm().locale,
                        startDate: moment(end),
                    });
                    $("#form-endOn").daterangepicker({
                        timePicker: false,
                        singleDatePicker: true,
                        showDropdowns: true,
                        locale: getPickerTerm().locale,
                        startDate: moment(repeatEnd),
                    });
                    if (getPickerTerm().locale) {
                        clearInterval(loopstart);
                    }
                }
            } catch (error) { }
        }, 100);
    } else {
        let loop = setInterval(() => {
            try {
                $("#form-eventStart").daterangepicker({
                    timePicker: true,
                    singleDatePicker: true,
                    showDropdowns: true,
                    timePicker24Hour: true,
                    locale: getPickerTerm().locale,
                    startDate: moment(),
                });
                $("#form-eventEnd").daterangepicker({
                    timePicker: true,
                    singleDatePicker: true,
                    showDropdowns: true,
                    timePicker24Hour: true,
                    locale: getPickerTerm().locale,
                    startDate: moment().add(4, "hours"),
                });
                $("#form-endOn").daterangepicker({
                    timePicker: false,
                    singleDatePicker: true,
                    showDropdowns: true,
                    locale: getPickerTerm().locale,
                    startDate: moment(),
                });
                if (getPickerTerm().locale) {
                    clearInterval(loop);
                }
            } catch (error) { }
        }, 100);
    }
}

function initilizeRepeat() {
    $("input").on("change", () => {
        calRepeat();
    });
    $("#form-weeklyRepeat > button").click(function () {
        $(this).toggleClass("btn-primary");
        $(this).toggleClass("btn-light");
    });
    $("#form-repeatFreq").select2({
        language: lang,
        minimumResultsForSearch: Infinity,
        data: freq,
    });
    $("#repeatRow").hide();
    $("#form-endOn").prop("disabled", true);
    $("#form-endOn").val(moment().format("YYYY-MM-DD"));
    $("#form-afterCheck").prop("disabled", true);
    $("#form-eventStart").val(moment().format("YYYY-MM-DDThh:mm"));
    $("#form-eventEnd").val(moment().add(4, "hours").format("YYYY-MM-DDThh:mm"));
    $("input#form-Repeat").on("click", function () {
        if ($("#form-Repeat:checked").val()) {
            $("#repeatRow").show();
            $(`#recursion`).show()
        } else {
            $("#repeatRow").hide();
            $(`#recursion`).hide()
        }
    });
    $("#form-YearlyMonth").val(moment().format("M")).trigger("change");

    $("#form-YearlyDay").val(moment().format("D"));
    checkWeekday();
}

function calRepeat() {
    $("#repeatString").val("");
    recurrenceRule = {
        FREQ: "",
        BYDAY: "",
        COUNT: "",
        UNTIL: "",
        INTERVAL: "",
        BYMONTHDAY: "",
        BYMONTH: "",
    };
    if ($("#form-Repeat:checked").val() == null) return;
    let key = $("#form-repeatFreq").val();
    let string = `FREQ=${key}`;
    recurrenceRule.FREQ = key;
    switch (key) {
        case "HOURLY":
            if ($("#interval").val() > 1) {
                string += `;INTERVAL=${$("#interval").val()}`;
                recurrenceRule.INTERVAL = $("#interval").val();
            }
            if ($("#form-onCheck:checked").val()) {
                string += `;UNTIL=${moment(
                    $("#form-endOn").val(),
                    getPickerTerm(localStorage.getItem("lang")).locale.format
                )
                    .utc()
                    .format("YYYYMMDDTHHmmss")}Z`;
                recurrenceRule.UNTIL =
                    moment(
                        $("#form-endOn").val(),
                        getPickerTerm(localStorage.getItem("lang")).locale.format
                    )
                        .utc()
                        .format("YYYYMMDDTHHmmss") + "Z";
            }
            if ($("#form-after-btn:checked").val()) {
                string += `;COUNT=${$("#form-afterCheck").val()}`;
                recurrenceRule.COUNT = $("#form-afterCheck").val();
            }
            break;
        case "DAILY":
            if ($("#interval").val() > 1) {
                string += `;INTERVAL=${$("#interval").val()}`;
                recurrenceRule.INTERVAL = $("#interval").val();
            }
            if ($("#form-onCheck:checked").val()) {
                string += `;UNTIL=${moment(
                    $("#form-endOn").val(),
                    getPickerTerm(localStorage.getItem("lang")).locale.format
                )
                    .utc()
                    .format("YYYYMMDDTHHmmss")}Z`;
                recurrenceRule.UNTIL =
                    moment(
                        $("#form-endOn").val(),
                        getPickerTerm(localStorage.getItem("lang")).locale.format
                    )
                        .utc()
                        .format("YYYYMMDDTHHmmss") + "Z";
            }
            if ($("#form-after-btn:checked").val()) {
                string += `;COUNT=${$("#form-afterCheck").val()}`;
                recurrenceRule.COUNT = $("#form-afterCheck").val();
            }
            break;
        case "WEEKLY":
            if ($("#interval").val() > 1) {
                string += `;INTERVAL=${$("#interval").val()}`;
                recurrenceRule.INTERVAL = $("#interval").val();
            }
            if ($(".weekday.btn-primary").length > 0) {
                let arr = [];
                for (let i = 0; i < $(".weekday.btn-primary").length; i++) {
                    const element = $(".weekday.btn-primary")[i].id;
                    arr.push(element);
                }
                string += `;BYDAY=${arr.join(",")}`;
                recurrenceRule.BYDAY = arr.join(",");
            }
            if ($("#form-onCheck:checked").val()) {
                string += `;UNTIL=${moment(
                    $("#form-endOn").val(),
                    getPickerTerm(localStorage.getItem("lang")).locale.format
                )
                    .utc()
                    .format("YYYYMMDDTHHmmss")}Z`;
                recurrenceRule.UNTIL =
                    moment(
                        $("#form-endOn").val(),
                        getPickerTerm(localStorage.getItem("lang")).locale.format
                    )
                        .utc()
                        .format("YYYYMMDDTHHmmss") + "Z";
            }
            if ($("#form-after-btn:checked").val()) {
                string += `;COUNT=${$("#form-afterCheck").val()}`;
                recurrenceRule.COUNT = $("#form-afterCheck").val();
            }
            break;
        case "MONTHLY":
            if ($("#interval").val() > 1) {
                string += `;INTERVAL=${$("#interval").val()}`;
                recurrenceRule.INTERVAL = $("#interval").val();
            }
            if ($("#form-onCheck:checked").val()) {
                string += `;UNTIL=${moment(
                    $("#form-endOn").val(),
                    getPickerTerm(localStorage.getItem("lang")).locale.format
                )
                    .utc()
                    .format("YYYYMMDDTHHmmss")}Z`;
                recurrenceRule.UNTIL =
                    moment(
                        $("#form-endOn").val(),
                        getPickerTerm(localStorage.getItem("lang")).locale.format
                    )
                        .utc()
                        .format("YYYYMMDDTHHmmss") + "Z";
            }
            if ($("#form-after-btn:checked").val()) {
                string += `;COUNT=${$("#form-afterCheck").val()}`;
                recurrenceRule.COUNT = $("#form-afterCheck").val();
            }
            break;
        case "YEARLY":
            if ($("#interval").val() > 1) {
                string += `;INTERVAL=${$("#interval").val()}`;
                recurrenceRule.INTERVAL = $("#interval").val();
            }
            if ($("#form-YearlyMonth").val() > 0) {
                string += `;BYMONTHDAY=${$("#form-YearlyDay").val()};BYMONTH=${$(
                    "#form-YearlyMonth"
                ).val()}`;
                recurrenceRule.BYMONTHDAY = $("#form-YearlyDay").val();
                recurrenceRule.BYMONTH = $("#form-YearlyMonth").val();
            }
            if ($("#form-onCheck:checked").val()) {
                string += `;UNTIL=${moment(
                    $("#form-endOn").val(),
                    getPickerTerm(localStorage.getItem("lang")).locale.format
                )
                    .utc()
                    .format("YYYYMMDDTHHmmss")}Z`;
                recurrenceRule.UNTIL =
                    moment(
                        $("#form-endOn").val(),
                        getPickerTerm(localStorage.getItem("lang")).locale.format
                    )
                        .utc()
                        .format("YYYYMMDDTHHmmss") + "Z";
            }
            if ($("#form-after-btn:checked").val()) {
                string += `;COUNT=${$("#form-afterCheck").val()}`;
                recurrenceRule.COUNT = $("#form-afterCheck").val();
            }
            break;
    }
    $("#repeatString").val(string);
}
function checkWeekday() {
    let weekday = moment().format("dd").toUpperCase();
    if ($("#form-weeklyRepeat > .btn-primary").length < 1) {
        $(`#${weekday}`).toggleClass("btn-primary");
        $(`#${weekday}`).toggleClass("btn-light");
    }
}

function changeFrequency(val) {
    switch (val) {
        case "HOURLY":
            $("#everyLabel").text(getTerm("hours"));
            $("#form-weekly").hide();
            $("#form-yearly").hide();
            break;
        case "DAILY":
            $("#everyLabel").text(getTerm("days"));
            $("#form-weekly").hide();
            $("#form-yearly").hide();
            break;
        case "WEEKLY":
            $("#everyLabel").text(getTerm("weeks"));
            $("#form-weekly").show();
            $("#form-yearly").hide();
            break;
        case "MONTHLY":
            $("#everyLabel").text(getTerm("months"));
            $("#form-weekly").hide();
            $("#form-yearly").hide();
            break;
        case "YEARLY":
            $("#everyLabel").text(getTerm("years"));
            $("#form-yearly").show();
            $("#form-weekly").hide();
            break;
        default:
            $("#everyLabel").text("");
            $("#form-weekly").hide();
            $("#form-yearly").hide();
            break;
    }
}

function getTerm(term) {
    let code = localStorage.getItem("lang");
    let translated;
    langs.forEach((e) => {
        if ((e.term == term) & (e.langCode == code)) {
            translated = e.translated;
        }
    });
    return translated;
}
// Business watcher
$("#buSelect").on("change", () => {
    initializeBusiness()
})
function initializeBusiness() {
    try {
        $("#moduleSelect").select2().select2("destroy");
    } catch (error) { }
    modules = [];
    let array = $("#buSelect").val();
    array.forEach((element) => {
        $.get(`/module/${element}`).done(function (data) {
            data.forEach(el => {
                modules.push({ id: el.id, text: el.name });
                let lang = localStorage.getItem("lang");
                $("#moduleSelect").select2({
                    language: lang,
                    data: modules,
                    multiple: true,
                });
            });
        });
    });
}
// Module watcher
$("#moduleSelect").on("change", () => {
    initializeDepartment()
})
function initializeDepartment() {
    try {
        $("#deptSelect").select2().select2("destroy");
    } catch (error) { }
    departments = [];
    let array = $("#moduleSelect").val();
    array.forEach((element) => {
        $.get(`/department/${element}`).done(function (data) {
            data.forEach(el => {
                departments.push({ id: el.id, text: el.name });
                let lang = localStorage.getItem("lang");
                setTimeout(() => {
                    $("#deptSelect").select2({
                        language: lang,
                        data: departments,
                        multiple: true,
                    });
                }, 100);
            });

        });
    });
}

// Department watcher
$("#deptSelect").on("change", () => {
    initializeArea()
})
function initializeArea() {
    try {
        $("#areaSelect").select2().select2("destroy");
    } catch (error) { }
    areas = [];
    let array = $("#deptSelect").val();
    array.forEach((element) => {
        $.get(`/area/${element}`).done(function (data) {
            data.forEach(el => {
                areas.push({ id: el.id, text: el.name });
                let lang = localStorage.getItem("lang");
                setTimeout(() => {
                    $("#areaSelect").select2({
                        language: lang,
                        data: areas,
                        multiple: true,
                    });
                }, 100);
            });

        });
    });
}

function getQuestions(from, id) {
    let response = []
    $.get(`/${from}_questions/${id}`).done(function (data) {
        data.forEach(element => {
            populateQuestionIds(element.id)
        });
    })
    return response
}

function getQuestion(id) {
    $.get(`/question/${id}`).done(function (data) {
        data.forEach(element => {
            populateQuestionBank(element)
        });
    })
}

function populateQuestionIds(id) {
    if (!question_ids.includes(id)) {
        question_ids.push(id)
    }
}

function populateQuestionBank(item) {
    $('#questionsRow').html('')
    questionBank.push(item)
    if (questionBank) {
        questionBank.forEach((e) => {
            let required = ''
            let required_star = ''
            if (e.required) {
                required = 'required'
                required_star = '*'
            }
            $('#questionsRow').append(`
        <div class="col-6">
            <div class="row">
                <div class="col">
                    <label class="dtContributor"><strong>${required_star}</strong> ${e.name}</label>
                    <div class="form-group">
                        <textarea type="text" class="w-100 p-2" onchange="populateQuestionResponse()" id="${e.id}" ${required}></textarea>
                    </div>
                </div>
            </div>
        </div>`)
        })
    }
    setTimeout(() => {
        try {
            var question_response = JSON.parse(sessionStorage.getItem('question_response'))
            question_response.forEach((e) => {
                $(`#${e.q_id}`).val(`${e.response}`)
            })
        } catch (error) {

        }

    }, 200);
}

function getApprovers(from, id) {
    let response = []
    $.get(`/${from}_approvers/${id}`).done(function (data) {
        data.forEach(element => {
            populateApproverIds(element.user_id)
            populateApproverIds_(element.id)
        });
    })
    return response
}

function getApprover(id) {
    $.get(`/user/${id}`).done(function (data) {
        data.forEach(element => {
            populateApproverBank(element)
        });
    })
}

function populateApproverIds(id) {
    if (!approver_ids.includes(id)) {
        approver_ids.push(id)
    }
}

function populateApproverIds_(id) {
    if (!approver_ids_.includes(id)) {
        approver_ids_.push(id)
    }
}

function populateApproverBank(item) {
    approverBank.push(item)
    if (approverBank.length > 0) {
        let $html = '<ul class="list-inline pl-5 bg-light">'
        approverBank.forEach((e) => {
            $html += `<li class="list-inline-item">${e.email}</li>`
        })
        $html += '</ul>'
        $('#form-approver').html($html)
    }
    populateApproversResponse()
}

function getContributors(from, id) {
    let response = []
    $.get(`/${from}_contributors/${id}`).done(function (data) {
        data.forEach(element => {
            populateContributorsIds(element.user_id)
            populateContributorsIds_(element.id)
        });
    })
    return response
}

function getContributor(id) {
    $.get(`/user/${id}`).done(function (data) {
        data.forEach(element => {
            populateContributorBank(element)
        });
    })
}

function populateContributorsIds(id) {
    if (!contributor_ids.includes(id)) {
        contributor_ids.push(id)
    }
}

function populateContributorsIds_(id) {
    if (!contributor_ids_.includes(id)) {
        contributor_ids_.push(id)
    }
}

function populateContributorBank(item) {
    contributorBank.push(item)
    if (contributorBank.length > 0) {
        let $html = '<ul class="list-inline pl-5 bg-light">'
        contributorBank.forEach((e) => {
            $html += `<li class="list-inline-item">${e.email}</li>`
        })
        $html += '</ul>'
        $('#form-contributor').html($html)
    }
    populateContributorsResponse()
}

function scan() {
    question_ids = []
    approver_ids = []
    contributor_ids = []
    $buSelect = $('#buSelect').val()
    $moduleSelect = $('#moduleSelect').val()
    $deptSelect = $('#deptSelect').val()
    $typeSelect = $('#typeSelect').val()
    $reasonSelect = $('#reasonSelect').val()
    if ($buSelect) {
        $buSelect.forEach(element => {
            getQuestions('business', element)
            getApprovers('business', element)
            getContributors('business', element)
        });
    }
    if ($moduleSelect) {
        $moduleSelect.forEach(element => {
            getQuestions('module', element)
            getApprovers('module', element)
            getContributors('module', element)
        });
    }
    if ($deptSelect) {
        $deptSelect.forEach(element => {
            getQuestions('department', element)
            getApprovers('department', element)
            getContributors('department', element)
        });
    }
    if ($reasonSelect) {
        $('#areaSelect').val().forEach(element => {
            getQuestions('area', element)
            getApprovers('area', element)
            getContributors('area', element)
        });
    }
    if ($typeSelect) {
        getQuestions('type', $typeSelect)
        getApprovers('type', $typeSelect)
        getContributors('type', $typeSelect)
    }
    if ($reasonSelect) {
        getQuestions('reason', $reasonSelect)
        getApprovers('reason', $reasonSelect)
        getContributors('reason', $reasonSelect)
    }
    //  *****************************************
    setTimeout(() => {
        questionBank = []
        if (question_ids.length > 0) {
            question_ids.forEach(element => {
                getQuestion(element)
            });
        }
        approverBank = []
        if (approver_ids.length > 0) {
            approver_ids.forEach(element => {
                getApprover(element)
            });
        }
        contributorBank = []
        if (contributor_ids.length > 0) {
            contributor_ids.forEach(element => {
                getContributor(element)
            });
        }
    }, 600);
    // ******************************************

    try {
        $('#start_date_formated').val(moment($('#form-eventStart').data().daterangepicker.startDate).utc().format())
        $('#end_date_formated').val(moment($('#form-eventEnd').data().daterangepicker.startDate).utc().format())
    } catch (error) {

    }
}

$('#buSelect').on('select2:select', () => {
    scan()
    populateBusinessResponse()
});
$('#moduleSelect').on('select2:select', () => {
    scan()
    populateModuleResponse()
});
$('#deptSelect').on('select2:select', () => {
    scan()
    populateDepartmentResponse()
});
$('#areaSelect').on('select2:select', () => {
    scan()
    populateAreaeResponse()
});
$('#typeSelect').on('select2:select', () => {
    scan()
});
$('#reasonSelect').on('select2:select', () => {
    scan()
});

function populateQuestionResponse() {

    let question_response = []
    question_ids.forEach((e) => {
        question_response.push({ id: e, response: $(`#${e}`).val() })
    })
    $('#question_response').val(JSON.stringify(question_response))
}

function populateApproversResponse() {
    $('#approval_response').val(JSON.stringify(approver_ids_))
}

function populateContributorsResponse() {
    $('#contributor_response').val(JSON.stringify(contributor_ids_))
}

function populateBusinessResponse() {
    $('#business_ids').val(JSON.stringify($('#buSelect').val()))
}

function populateModuleResponse() {
    $('#module_ids').val(JSON.stringify($('#moduleSelect').val()))
}

function populateDepartmentResponse() {
    $('#department_ids').val(JSON.stringify($('#deptSelect').val()))
}

function populateAreaeResponse() {
    $('#area_ids').val(JSON.stringify($('#areaSelect').val()))
}

$('#form-eventStart').on('apply.daterangepicker', function (ev, picker) {
    $('#start_date_formated').val(moment($('#form-eventStart').data().daterangepicker.startDate).utc().format())
    $('#end_date_formated').val(moment($('#form-eventEnd').data().daterangepicker.startDate).utc().format())
});

$('#form-eventEnd').on('apply.daterangepicker', function (ev, picker) {
    $('#start_date_formated').val(moment($('#form-eventStart').data().daterangepicker.startDate).utc().format())
    $('#end_date_formated').val(moment($('#form-eventEnd').data().daterangepicker.startDate).utc().format())
});


if (sessionStorage.getItem('backTo')) {
    $(`#navOptions`).show()
} else {
    $(`#navOptions`).hide()
}