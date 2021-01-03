
$(document).ready(function () {
    var filtered_status = $('#filtered_status').val()
    var filtered_type = $('#filtered_type').val()
    var filtered_reason = $('#filtered_reason').val()
    var filtered_business = $('#filtered_business').val()
    var filtered_module = $('#filtered_module').val()
    var filtered_department = $('#filtered_department').val()
    var filtered_area = $('#filtered_area').val()

    $('.filtered_status').on('change', (e) => {
        filtered_status = e.target.value;
        data_store.load()
    })
    $('.filtered_type').on('change', (e) => {
        filtered_type = e.target.value;
        data_store.load()
    })
    $('.filtered_reason').on('change', (e) => {
        filtered_reason = e.target.value;
        data_store.load()
    })
    $('.filtered_business').on('change', (e) => {
        filtered_business = e.target.value;
        data_store.load()
    })
    $('.filtered_module').on('change', (e) => {
        filtered_module = e.target.value;
        data_store.load()
    })
    $('.filtered_department').on('change', (e) => {
        filtered_department = e.target.value;
        data_store.load()
    })
    $('.filtered_area').on('change', (e) => {
        filtered_area = e.target.value;
        data_store.load()
    })
    var data_store = new DevExpress.data.DataSource({
        store: new DevExpress.data.CustomStore({

            load: function (loadOptions) {
                args = {};
                let startDate, endDate;
                [
                    "filter",
                ].forEach(function (i) {
                    if (i in loadOptions && isNotEmpty(loadOptions[i]))
                        args[i] = JSON.stringify(loadOptions[i]);
                    try {
                        startDate = moment(loadOptions[i][0][4][0][1]).format('YYYY-MM-DD');
                        endDate = moment(loadOptions[i][0][0][1][2]).format('YYYY-MM-DD');
                    } catch (error) {

                    }
                });

                var result = $.Deferred();

                $.ajax({
                    data: {
                        start_date: startDate,
                        end_date: endDate,
                        status: filtered_status,
                        type: filtered_type,
                        reason: filtered_reason,
                        business: filtered_business,
                        module: filtered_module,
                        department: filtered_department,
                        area: filtered_area,
                    },
                    type: 'GET',
                    url: [
                        "/calendar_api"
                    ].join("")
                }).done(function (response) {

                    result.resolve(response.items);
                });

                return result.promise();
            }
        })
    })



    function isNotEmpty(value) {
        return value !== undefined && value !== null && value !== "";
    }
    $("#scheduler").dxScheduler({
        dataSource: data_store,
        timeZone: "America/New_York",
        firstDayOfWeek: 0,
        startDayHour: 0,
        endDayHour: 23,
        showAllDayPanel: false,
        height: 600,
        crossScrollingEnabled: true,
        remoteFiltering: true,
        showCurrentTimeIndicator: true,
        shadeUntilCurrentTime: true,
        editing: {
            allowAdding: false,
            allowDragging: false
        },
        editing: false,
        firstDayOfWeek: 0,
        remoteFiltering: true,
        views: ["month"],
        currentView: "month",
        resources: [{
            fieldExpr: "status_id",
            dataSource: [{ id: 1, color: '#ffc107' }, { id: 2, color: '#28a745' }, { id: 3, color: 'red' }],
            useColorAsDefault: true
        }],
        // appointmentTemplate: function (model) {

        //     return $("<div class='showtime-preview'>" +
        //         "<div>" + model.appointmentData.text + "</div>" +
        //         "<div><strong>" + model.appointmentData.status + "</strong>" +
        //         "</div>" +
        //         // "<div>" + model.appointmentData.startDate +
        //         // " - " + model.appointmentData.endDate +
        //         "</div>" +
        //         "</div>");
        // },
        onAppointmentClick: function (e) {
            $("#loader").show();
            setBackTo(window.location.pathname);
            window.location = `/request/${e.appointmentData.id}`;
        },
        onAppointmentDblClick: function (e) {
            $("#loader").show();
            setBackTo(window.location.pathname);
            window.location = `/request/${e.appointmentData.id}`;
        }
    });








    function isNotEmpty(value) {
        return value !== undefined && value !== null && value !== "";
    }
    $("#timeline").dxScheduler({
        dataSource: data_store,
        timeZone: "America/New_York",
        firstDayOfWeek: 0,
        startDayHour: 0,
        endDayHour: 23,
        showAllDayPanel: false,
        height: 600,
        crossScrollingEnabled: true,
        remoteFiltering: true,
        showCurrentTimeIndicator: true,
        shadeUntilCurrentTime: true,
        editing: {
            allowAdding: false,
            allowDragging: false
        },
        editing: false,
        firstDayOfWeek: 0,
        remoteFiltering: true,
        views: ["agenda", "timelineDay", "timelineWeek", "timelineMonth"],
        currentView: "agenda",
        resources: [{
            fieldExpr: "status_id",
            dataSource: [{ id: 1, color: '#ffc107' }, { id: 2, color: '#28a745' }, { id: 3, color: 'red' }],
            useColorAsDefault: true
        }],

        onAppointmentClick: function (e) {
            $("#loader").show();
            setBackTo(window.location.pathname);
            window.location = `/request/${e.appointmentData.id}`;
        },
        onAppointmentDblClick: function (e) {
            $("#loader").show();
            setBackTo(window.location.pathname);
            window.location = `/request/${e.appointmentData.id}`;
        }
    });

});

function navBack() {
    window.location = sessionStorage.getItem("backTo");
    sessionStorage.removeItem("backTo");
}

function setBackTo_edit(backTo) {
    sessionStorage.setItem("backTo_edit", backTo);
}
function navBack_edit() {
    window.location = sessionStorage.getItem("backTo_edit");
    sessionStorage.removeItem("backTo_edit");
}

function setBackTo(backTo) {
    sessionStorage.setItem("backTo", backTo);
}