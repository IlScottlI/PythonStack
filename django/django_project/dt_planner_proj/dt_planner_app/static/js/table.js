
$('#pageSize').on('change', () => {
    getTableData(`/api/users/?page[number]=1&page[size]=${$('#pageSize').val()}`)
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

getTableData(`/api/users/?page[number]=1&page[size]=${$('#pageSize').val()}`)

function getTableData(url) {
    $.get(url, function (data) {
        console.log(data)
        $("#users").html(
            () => {
                let string = ''
                let admin = 'checked'
                data.data.forEach((e) => {
                    if (e.attributes.admin) {
                        admin = 'checked'
                    } else {
                        admin = ''
                    }
                    string +=
                        `<tr>
                <td>${e.attributes.first_name} ${e.attributes.last_name}</td>
                <td>${e.attributes.email}</td>
                <td>${e.attributes.plant.name}</td>
                <td><input type="checkbox" ${admin} style="width: 1.25rem;height: 1.25rem;" onclick="return false;"/></td>
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