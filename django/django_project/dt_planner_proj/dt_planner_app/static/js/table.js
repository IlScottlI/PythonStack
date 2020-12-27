
$('#pageSize').on('change', () => {
    getTableData(`/api/calendars/?page[number]=1&page[size]=${$('#pageSize').val()}`)
})
$('#business_select').on('change', () => {
    getTableData(`/api/calendars/?page[number]=1&page[size]=${$('#pageSize').val()}`)
})
$('#module_select').on('change', () => {
    getTableData(`/api/calendars/?page[number]=1&page[size]=${$('#pageSize').val()}`)
})
$('#department_select').on('change', () => {
    getTableData(`/api/calendars/?page[number]=1&page[size]=${$('#pageSize').val()}`)
})
$('#area_select').on('change', () => {
    getTableData(`/api/calendars/?page[number]=1&page[size]=${$('#pageSize').val()}`)
})




function buildPagination(links, pages, page) {
    let li_s = '', active = ''
    for (let i = 1; i <= pages; i++) {
        if (i == page) {
            active = 'active'
        } else {
            active = ''
        }
        li_s += `<li class="page-item ${active}"><a class="page-link" onclick="getTableData('/api/users/?page[number]=${i}&page[size]=${$('#pageSize').val()}')">${i}</a></li>`
    }
    let prev_disabled = 'disabled'
    if (links.prev) {
        prev_disabled = ''
    } else {
        prev_disabled = 'disabled'
    }
    let next_disabled = 'disabled'
    if (links.next) {
        next_disabled = ''
    } else {
        next_disabled = 'disabled'
    }
    return `
      <li class="page-item ${prev_disabled}" id="prev" ${prev_disabled}>
            <a class="page-link ${prev_disabled}" onclick="getTableData('${links.prev}')" aria-label="Previous" ${prev_disabled}>
                <span aria-hidden="true">«</span>
            </a>
        </li>
        ` + `
        ${li_s}
        ` +
        `
        <li class="page-item ${next_disabled}" ${next_disabled}>
            <a class="page-link ${next_disabled}" onclick="getTableData('${links.next}')" aria-label="Next" ${next_disabled}>
                <span aria-hidden="true">»</span>
            </a>
        </li>
    `
}

getTableData(`/api/calendars/?page[number]=1&page[size]=${$('#pageSize').val()}`)

function getTableData(url) {
    $.get(url, function (data) {
        $("#approvals").html(
            () => {
                let string = ''
                let admin = 'checked'
                let modules = []
                let departments = []
                let areas = []
                data.data.forEach((e) => {
                    modules = []
                    try {
                        e.attributes.module.forEach((el) => {
                            modules.push(el.name)
                        })
                    } catch { }
                    departments = []
                    try {
                        e.attributes.department.forEach((el) => {
                            departments.push(el.name)
                        })
                    } catch { }
                    if (e.attributes.admin) {
                        admin = 'checked'
                    } else {
                        admin = ''
                    }
                    areas = []
                    try {
                        e.attributes.area.forEach((el) => {
                            areas.push(el.name)
                        })
                    } catch { }
                    string +=
                        `<tr>
                <td>${e.attributes.title} </td>
                <td>${moment(e.attributes.start_date).format('MM/D/YY h:mm a')}<br>
                ${moment(e.attributes.end_date).format('MM/D/YY h:mm a')}
                </td>
                <td>${modules.join(', ')}</td>
                <td>${departments.join(', ')}</td>
                <td>${areas.join(', ')}</td>
                <td>${e.attributes.types.name}</td>
                <td class="btn btn-${e.attributes.status.color} text-sm-center btn-block" onclick="setBackTo(window.location.pathname);window.location = '/request/${e.id}'">${e.attributes.status.name}</td>
                <td>${e.attributes.owner.first_name} ${e.attributes.owner.last_name}</td>
              </tr>` })
                $('#dataTable_info').text(
                    `Showing ${data.meta.pagination.page} to ${data.meta.pagination.pages} of ${data.meta.pagination.count}`
                )
                $('#pagination').html(buildPagination(data.links, data.meta.pagination.pages, data.meta.pagination.page))
                return string
            }
        );
    });
}



