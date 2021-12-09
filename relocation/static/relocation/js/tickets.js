$(document).ready(function() {

    $("input[name='type']").change(() => {
        const inputs = ['#departure-name', '#departure-id','#arrival-name', '#arrival-id'];
        inputs.forEach((input) => { $(input).val('') });
    });


    const stationsSettings = {
        bus:{
            url: "/relocation/stations",
            supplier: "ubus_busfor"
        },
        train:{
            url: "/relocation/stations",
            supplier: "uz_train"
        },
    };


    function setupStationInputs(station_name_selector, station_id_selector) {

        $(station_name_selector).autocomplete();

        $(station_name_selector).on('input', event => {

            const search_string = $(event.currentTarget).val();
            const type = $("input[name='type']:checked").val();
            const url = stationsSettings[type].url;
            const supplier = stationsSettings[type].supplier;
            const language = $('html').prop('lang') || 'uk';

            if (search_string.length > 0) {
                $.ajax({
                    type: "POST",
                    url: url,
                    headers: {
                        'language': language,
                        'supplier': supplier,
                        'content-type': 'application/json'
                    },

                    data: JSON.stringify({
                        "language": language,
                        "supplier": supplier,
                        "query": search_string,
                        "type": type
                    }),

                    success: function (response) {
                        function identify_id(stations, station_name) {
                            let chosen_station = stations.find(station => {
                                return station.name.toLowerCase() === station_name.toLowerCase()
                            });

                            if (chosen_station && chosen_station.id != null) {
                                $(station_id_selector).val(chosen_station.id);
                            }
                        }

                        let loaded_stations = response['stations'];

                        $(event.currentTarget).autocomplete({
                            source: loaded_stations.map(station => station.name),
                            select: (event, ui) => {identify_id(loaded_stations, ui.item.value);}
                        });

                        identify_id(loaded_stations, search_string);
                    },
                    error: function (response) {
                        console.log(response.statusText);
                    }
                });
            }
        });
    }

    setupStationInputs('#departure-name', '#departure-id');
    setupStationInputs('#arrival-name', '#arrival-id');

});