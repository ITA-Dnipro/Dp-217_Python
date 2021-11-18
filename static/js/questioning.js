async function getQuestions(val) {
    let url = '/questioning/questions/' + val;
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function ajaxRequest(values, answer_id) {
    //let csrf = $('input[name=csrfmiddlewaretoken]')[0].value;
    if ((typeof values == "undefined") || (typeof values == "number")) {
        let questions = await getQuestions(values);
        values = JSON.parse(questions);
    } else {
        values['results'][answer_id[0]] += answer_id[1];
    }
    if (values['questions'].length > 1) {
        let val = values['questions'].pop();
        for (let index = 0; index < values['buttons'].length; index++) {
            val['answers'][index]['btn'] = values['buttons'][index]
        }
        let SendInfo = {
            question: val['question'],
            answers: val['answers'],
            values: values
        };
        $.ajax({
            type: "POST",
            url: '/questioning/questions/',
            data: JSON.stringify(SendInfo),
            dataType: 'text',
            success: function (res) {
                $("#main_container").html(res);
            },
            error: function (res, error) {
                console.log(error);
            }
        });
    } else {
        $.ajax({
            type: "POST",
            url: '/questioning/results/',
            data: JSON.stringify([values['type'], values['results']]),
            dataType: 'text',
            success: function (res) {
                let start_index = res.indexOf('<div id="results">', 0);
                let end_index = res.length;
                let resp = '';
                for (let i = start_index; i < end_index; i++) {
                    resp = resp + res[i];
                }
                $("#main_container").html(resp);
            },
            error: function (res, error) {
                console.log(error);
            }
        });
    }
}
