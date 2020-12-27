
try {
    $('#textarea_comment').on('keyup', () => {
        $('#update_comment').val($('#textarea_comment').val())
        if ($('#textarea_comment').val().length > 2) {
            $('#comment_update_btn').attr('disabled', false)
        } else {
            $('#comment_update_btn').attr('disabled', true)
        }
    })

    $('#comment_update_btn').on('click', () => {
        $('#update_submit').click()
    })

    try {
        let object = {}
        sessionStorage.getItem('recurrenceRule').split(';').forEach((e) => {
            temp = e.split('=')
            let key = temp[0]
            let value = temp[1]
            object[key] = value
        })
        rules = object
        changeFrequency(rules.FREQ); calRepeat();
    } catch (error) {

    }




    $.ajax({ url: `/question_response/${sessionStorage.getItem('id')}` }).done(function (response) {
        sessionStorage.setItem('question_response', JSON.stringify(response))
        setTimeout(() => {
            try {
                var question_response = JSON.parse(sessionStorage.getItem('question_response'))
                question_response.forEach((e) => {
                    $(`#${e.q_id}`).val(`${e.response}`)
                })
            } catch (error) {

            }

        }, 200);
    });
    setTimeout(() => {
        if (sessionStorage.getItem('b_ids')) {
            var b_ids = sessionStorage.getItem('b_ids').split(',')
        }
        try {
            $('#buSelect').val(b_ids)
            $('#buSelect').trigger('change')
            $('#business_ids').val(JSON.stringify(b_ids))
        } catch {

        }
        setTimeout(() => {
            if (sessionStorage.getItem('m_ids')) {
                var m_ids = sessionStorage.getItem('m_ids').split(',')
            }
            try {
                $('#moduleSelect').val(m_ids)
                $('#moduleSelect').trigger('change')

                $('#module_ids').val(JSON.stringify(m_ids))
            } catch {

            }
            setTimeout(() => {
                if (sessionStorage.getItem('d_ids')) {
                    var d_ids = sessionStorage.getItem('d_ids').split(',')
                }
                try {
                    $('#deptSelect').val(d_ids)
                    $('#deptSelect').trigger('change')
                    $('#department_ids').val(JSON.stringify(d_ids))
                } catch {

                }
                setTimeout(() => {
                    if (sessionStorage.getItem('a_ids')) {
                        var a_ids = sessionStorage.getItem('a_ids').split(',')
                    }
                    try {
                        $('#areaSelect').val(a_ids)
                        $('#areaSelect').trigger('change')
                        $('#area_ids').val(JSON.stringify(a_ids))
                    } catch {

                    }
                    scan()
                    if (sessionStorage.getItem('start_date')) {
                        let start_date = sessionStorage.getItem('start_date')
                        $("#form-eventStart").daterangepicker({
                            timePicker: true,
                            singleDatePicker: true,
                            showDropdowns: true,
                            timePicker24Hour: true,
                            locale: getPickerTerm().locale,
                            startDate: moment(start_date),
                        })
                    }
                    if (sessionStorage.getItem('end_date')) {
                        let end_date = sessionStorage.getItem('end_date')
                        $("#form-eventEnd").daterangepicker({
                            timePicker: true,
                            singleDatePicker: true,
                            showDropdowns: true,
                            timePicker24Hour: true,
                            locale: getPickerTerm().locale,
                            startDate: moment(end_date),
                        })
                    }
                    if ($("#form-Repeat:checked").val()) {
                        $("#repeatRow").show();
                        $(`#recursion`).show()
                    } else {
                        $("#repeatRow").hide();
                        $(`#recursion`).hide()
                    }
                    setTimeout(() => {
                        $('#loader').hide()
                    }, 1000);
                    try {
                        if (rules.FREQ) {
                            $(`#form-repeatFreq`).val(rules.FREQ)
                            $(`#form-repeatFreq`).trigger("change")
                        }
                    } catch (error) {

                    }
                    try {
                        if (rules.INTERVAL) {
                            $("#interval").val(rules.INTERVAL)
                        } else {
                            $("#interval").val(1)
                        }
                    } catch (error) {

                    }
                    try {
                        if (rules.UNTIL) {
                            $("#form-endOn").daterangepicker({
                                timePicker: false,
                                singleDatePicker: true,
                                showDropdowns: true,
                                locale: getPickerTerm().locale,
                                startDate: moment(rules.UNTIL),
                            });
                            $('#form-onCheck').click()
                        }
                    } catch (error) {

                    }
                    try {
                        if (rules.BYDAY) {
                            $(`.weekday`).removeClass("btn-primary");
                            $(`.weekday`).removeClass("btn-light");
                            $(`.weekday`).toggleClass("btn-light");

                            let array = rules.BYDAY.split(',')
                            array.forEach(element => {
                                $(`#${element}`).toggleClass("btn-primary");
                                $(`#${element}`).toggleClass("btn-light");
                            });
                        }
                    } catch (error) {

                    }
                    try {
                        if (rules.COUNT) {
                            $('#form-after-btn').click()
                            $('#form-afterCheck').val(rules.COUNT)
                        }
                    } catch (error) {

                    }
                    try {
                        if (rules.BYMONTH) {
                            $(`#form-YearlyMonth`).val(rules.BYMONTH)
                            $(`#form-YearlyMonth`).trigger("change")
                        }
                    } catch (error) {

                    }
                    try {
                        if (rules.BYMONTHDAY) {
                            $(`#form-YearlyDay`).val(rules.BYMONTHDAY)
                        }
                    } catch (error) {

                    }
                    $("#update_form").submit(function (e) {
                        e.preventDefault();
                    });
                }, 200);
            }, 200);
        }, 200);
    }, 200);


} catch (error) {

}

function update_time() {
    $('#start_date_formated').val(moment($('#form-eventStart').data().daterangepicker.startDate).utc().format())
    $('#end_date_formated').val(moment($('#form-eventEnd').data().daterangepicker.startDate).utc().format())
}




