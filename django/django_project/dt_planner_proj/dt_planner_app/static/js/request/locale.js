


if (localStorage.getItem('lang')) {

} else {
    localStorage.setItem('lang', 'en')
}

var langs = [];
var langs_datePicker = [];
var langMenuItems = [];
var month = [];
var recurrenceRule = { FREQ: "", BYDAY: "", COUNT: "", UNTIL: "", INTERVAL: "", BYMONTHDAY: "", BYMONTH: "" };
var selectedRequest = {};
var result = {};
var freq = [];




$(document).ready(() => {
    lang = localStorage.getItem('lang')
    var count = 1000
    var langLoop = setInterval(() => {
        $('.select2-results__message').text(getTerm('itemsNotFound'))
        $('#goBtn').text(getTerm('goBtn'))
        $('.appTitle').text(getTerm('appTitle'))
        $('.newRequest').html('<i class="fa fa-plus d-inline-block mr-2" style="color: #96938e;"></i>' + getTerm('newRequest'))
        $('.viewRequest').html('<i class="fa fa-bars d-inline-block mr-2" style="color: #96938e;"></i>' + getTerm('viewRequest'))
        $('.dtCalendar').html('<i class="fa fa-calendar d-inline-block mr-2" style="color: #96938e;"></i>' + getTerm('dtCalendar'))
        $('.dtDashboard').html('<i class="fa fa-bar-chart d-inline-block mr-2" style="color: #96938e;"></i>' + getTerm('dtDashboard'))
        // $('.approvals').html('<span class="badge badge-secondary approvalCount mr-2"></span>' + getTerm('approvals')) // Removed because of Django Templates
        $('.projectName').text('*  ' + getTerm('projectName'))
        $('.dtOwner').text('*  ' + getTerm('dtOwner'))
        $('.business').text('*  ' + getTerm('business'))
        $('.module').text(getTerm('module'))
        $('.department').text(getTerm('department'))
        $('.area').text(getTerm('area'))
        $('.requestType').text('*  ' + getTerm('requestType'))
        $('.dtReasonCode').text('*  ' + getTerm('dtReasonCode'))
        $('.dateStart').text('*  ' + getTerm('dateStart'))
        $('.dateEnd').text('*  ' + getTerm('dateEnd'))
        $('.frequency').text(getTerm('frequency'))
        $('.every').text(getTerm('every'))
        $('.endRepeat').text(getTerm('endRepeat'))
        $('.never').text(getTerm('never'))
        $('.on').text(getTerm('on'))
        $('.after').text(getTerm('after'))
        $('.repeatOn').text(getTerm('repeatOn'))
        $('.sun').text(getTerm('sun'))
        $('.mon').text(getTerm('mon'))
        $('.tue').text(getTerm('tue'))
        $('.wed').text(getTerm('wed'))
        $('.thu').text(getTerm('thu'))
        $('.fri').text(getTerm('fri'))
        $('.sat').text(getTerm('sat'))
        $('.back').text(getTerm('back'))
        $('#updateBtn').text(getTerm('updateBtn'))
        $('#submitBtn').text(getTerm('submitBtn'))
        // changeFrequency($('#form-repeatFreq').val());
        $('.back').text(getTerm('back'))
        $('.status').text(getTerm('status'))
        $('.type').text(getTerm('type'))
        $('.dtReason').text(getTerm('dtReason'))
        $('.business').text(getTerm('business'))
        $('.module').text(getTerm('module'))
        $('.department').text(getTerm('department'))
        $('.area').text(getTerm('area'))

        month = [
            { id: 1, text: getTerm('jan') },
            { id: 2, text: getTerm('feb') },
            { id: 3, text: getTerm('mar') },
            { id: 4, text: getTerm('apr') },
            { id: 5, text: getTerm('may') },
            { id: 6, text: getTerm('jun') },
            { id: 7, text: getTerm('jul') },
            { id: 8, text: getTerm('aug') },
            { id: 9, text: getTerm('sep') },
            { id: 10, text: getTerm('oct') },
            { id: 11, text: getTerm('nov') },
            { id: 12, text: getTerm('dec') },
        ]
        freq = [
            { id: "HOURLY", text: getTerm('hourly') },
            { id: "DAILY", text: getTerm('daily') },
            { id: "WEEKLY", text: getTerm('weekly') },
            { id: "MONTHLY", text: getTerm('monthly') },
            { id: "YEARLY", text: getTerm('yearly') },
        ]

        if (count < 1) {
            clearInterval(langLoop)

        } else {
            count--
        }
    })
})
async function getLanguage() {
    await loadJson(`/locale`, {
    })
        .then((res) => {
            res.forEach((element) => {
                langMenuItems.push({ langCode: element.name, language: element.language })

                let JSON_Data = element.JSON_Data;
                try {
                    let datePickerJSON = element.date_picker
                    langs_datePicker.push({ langCode: element.name, locale: datePickerJSON.locale });
                } catch (error) {

                }
                JSON_Data.forEach((e) => {

                    langs.push({
                        term: e.term,
                        Title: e.enTrans,
                        langCode: e.langCode,
                        translated: e.translated,
                    });
                })
            });
            sessionStorage.setItem("langs", JSON.stringify(langs));

            let str = '<ul class="list-unstyled">'
            langMenuItems.forEach((e) => {
                str += `<li class="text-primary lang" id="${e.langCode}" onClick="initlizeLanguage('${e.langCode}'); window.location = ''; console.log('${e.langCode}')">${e.language}</li>`
            })
            $('#langMenu').html(`${str}</ul>`)
        })
        .catch((e) => {
            console.log(e)
        })
}

async function loadJson(url, headers) {
    // (1)
    let response = await fetch(url, headers); // (2)

    if (response.status == 200) {
        let json = await response.json(); // (3)

        return json;
    }

    throw new Error(response.status);
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


$('#form-repeatFreq').on('change', (e) => {
    if (e.target.value == 'YEARLY') {
        $("#form-YearlyMonth").select2({
            language: lang,
            minimumResultsForSearch: Infinity,
            data: month,
        });
    }
})

