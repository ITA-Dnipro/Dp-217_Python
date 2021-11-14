$(document).ready(function() {

    const filters = [
        {
            htmlName: 'region-select',
            dataName: 'region',
            stateName: 'region'
        },
        {
            htmlName: 'city-select',
            dataName: 'city',
            stateName: 'city'
        },
        {
            htmlName: 'university-select',
            dataName: 'university',
            stateName: 'university'
        }
    ];

    const defaultFiltersValue = 'Всі';

    let selectedValuesState = {
        region:defaultFiltersValue,
        city:defaultFiltersValue,
        university:defaultFiltersValue
    };

    let initialHousingsState = [];
    let housingsState = [];


    function setInitialHousingsState(housings) {
        initialHousingsState = [...housings];
    }


    function setHousingsState(housings) {
        housingsState = [...housings];
    }


    function setSelectedValuesState(newState) {
        selectedValuesState = {...newState}
    }


    function updateResultsTable() {
        $('#results-table > tbody').empty();
        housingsState.forEach(housing => {
            let columnsMarkup = `<td>${housing.name}</td>`;
            filters.forEach(filter => {
                columnsMarkup += `<td>${housing[filter.dataName]}</td>`
            });
            let row = `<tr>${columnsMarkup}</tr>`;
            $('#results-table > tbody:last-child').append(row);

        });
    }


    function init_filters(housings=initialHousingsState) {
        let regions = [defaultFiltersValue];
        let cities = [defaultFiltersValue];
        let universities = [defaultFiltersValue];
        let names = [];

        housings.forEach(housing => {
            regions.push(housing.region);
            cities.push(housing.city);
            universities.push(housing.university);
            names.push(housing.name);
        });

        regions = [...new Set(regions)];
        cities = [...new Set(cities)];
        universities = [...new Set(universities)];

        let regionSelect = $("#region-select");
        let citySelect = $("#city-select");
        let universitySelect = $("#university-select");

        regionSelect.empty();
        citySelect.empty();
        universitySelect.empty();

        regions.forEach(region => {
           regionSelect.append($("<option />").val(region).text(region))
        });

        cities.forEach(city => {
           citySelect.append($("<option />").val(city).text(city))
        });

        universities.forEach(university => {
           universitySelect.append($("<option />").val(university).text(university))
        });
    }


    function update_filters(housings=housingsState) {
        const filtersString = JSON.stringify(selectedValuesState);
        $("#result-output").html(filtersString);

        for (let i=0; i<filters.length; i++) {
            const htmlName = filters[i].htmlName;
            const dataName = filters[i].dataName;

            let newHousings = initialHousingsState.filter(function(housing) {
                let conditions = filters.map(filter => {
                    return (
                        dataName === filter.dataName
                        || selectedValuesState[filter.stateName] === defaultFiltersValue
                        || housing[filter.dataName] === selectedValuesState[filter.stateName]
                    )
                });

                return conditions.every(condition => condition===true);
            });

            $('#' + htmlName + ' option').prop("disabled", true);

            let options = [];

            newHousings.forEach(housing => {
                options.push(housing[dataName]);
            });

            options = [...new Set(options)];

            [defaultFiltersValue, ...options].forEach(option => {
                $('#' + htmlName + ' option:contains("'+ option +'")').prop('disabled', false);
            });

            let resultHousings = initialHousingsState.filter(function(housing) {
                let conditions = filters.map(filter => {
                    return (
                        selectedValuesState[filter.stateName] === defaultFiltersValue
                        || housing[filter.dataName] === selectedValuesState[filter.stateName]
                    )
                });

                return conditions.every(condition => condition===true);
            });

            setHousingsState(resultHousings);
            updateResultsTable();
        }
    }


    $("#region-select").on('change', function(){
        setSelectedValuesState({...selectedValuesState, region: this.value});
        update_filters();
    });


    $("#city-select").on('change', function(){
        setSelectedValuesState({...selectedValuesState, city: this.value});
        update_filters();
    });


    $("#university-select").on('change', function(){
        setSelectedValuesState({...selectedValuesState, university: this.value});
        update_filters();
    });


    $("#clear-filters-button").on('click', function () {
        setSelectedValuesState({
            region:defaultFiltersValue,
            city:defaultFiltersValue,
            university:defaultFiltersValue
        });
        update_filters();
    });

    // RUNS ON LOAD
    $.ajax({
        method: "GET",
        url: "/relocation/housings_json",
        success: function (response) {
            let housings = JSON.parse(response);
            setInitialHousingsState(housings);
            setHousingsState(initialHousingsState);
            init_filters();
            updateResultsTable();
        },
        error: function (response) {
            console.log(response.statusText);
        }
    });
});