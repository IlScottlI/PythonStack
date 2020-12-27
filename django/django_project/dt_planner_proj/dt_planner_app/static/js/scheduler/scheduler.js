function setBackTo(backTo) {
    sessionStorage.setItem("backTo", backTo);
}
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

var status = ''

$('.schedule_filter').on('change', (e) => {
    status = e.target.value;
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
                data: { start_date: startDate, end_date: endDate, status: status },
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
