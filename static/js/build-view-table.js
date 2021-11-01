function ajaxRemove(url) {
    $.ajax({
        type: "POST",
        url: '/questioning/results/remove/' + url,
        success: function (res) {
            $("#" + url).remove();
        },
        error: function (res, error) {
            console.log(error);
        }
    });
}

$(document).ready(function () {
    function generateTable(data) {
        let dataKey = data[0];
        let table = "<table>";
        table += "<thead><tr>";
        for (let key in dataKey) {
            table += "<th>" + dataKey[key] + "</th>";
        }
        table += "</tr></thead>";

        table += "<tbody>";
        for (let i = 1; i < data.length; i++) {
            table += '<tr class="table-light" id="' + data[i]['url'] + '">';
            let button = '<button onclick="ajaxRemove(\'' + data[i]['url'] + '\')">Видалити</button>';
            for (let j in data[i]) {
                if (j === 'date') {
                    table += '<td><a href="' + data[i]['url'] + '">' + data[i][j] + '</a></td>';
                } else if (j !== 'url') {
                    let cell = '';
                    for (let some_data in data[i][j]) {
                        cell += data[i][j][some_data];
                        if (some_data<data[i][j].length-1){
                            cell +=' , '
                        }
                    }
                    table += "<td>" + cell + "</td>";
                } else {
                    table += "<td>" + button + "</td>";
                }
            }
            table += "</tr>";
        }
        table += "</tbody></table>";

        document.getElementById("table").innerHTML = table;
    }

    function loadJson(selector) {
        return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
    }

    let jsonData = loadJson('#jsonData');
    generateTable(jsonData);
});
