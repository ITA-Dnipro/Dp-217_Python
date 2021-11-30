const regionsDataBox = document.getElementById('region-box')
const regionsInput = document.getElementById('regions')
const citiesDataBox = document.getElementById('cities-box')
const cityText = document.getElementById('city-text')

const fieldsDataBox = document.getElementById('field-box')
const fieldsInput = document.getElementById('fields')
const specialitiesDataBox = document.getElementById('specialities-box')
const specialityText = document.getElementById('speciality-text')

const searchButton = document.getElementById('btn-box')


searchButton.addEventListener('click', () => {
document.querySelector('.preloader').style.display = 'flex';
})


$.ajax({
    type: 'GET',
    url: '/search/region-data/',
    success: function(response){
        const regionsData = response.data
        console.log(regionsData)
        regionsData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.name)
            regionsDataBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})


regionsInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedRegion = e.target.value

    citiesDataBox.innerHTML = ""
    cityText.textContent = "Мiста"
    cityText.classList.add("default")


    $.ajax({
        type: 'GET',
        url: `cities-data/${selectedRegion}/`,
        success: function(response){
            const citiesData = response.data
            citiesData.map(item=>{
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.name)
                citiesDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
    })
})


$.ajax({
    type: 'GET',
    url: '/search/fields-data/',
    success: function (response) {
        const fieldsData = response.data
        fieldsData.map(item => {
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.name)
                fieldsDataBox.appendChild(option)
            }
        )
        let val = document.querySelector("#field_questioning").getAttribute('data');
        if (val !== '') {
            document.querySelector("#field_questioning").setAttribute('data', '');
            let event = new Event('change');
            $('#fields .default').html(val);
            document.getElementById('fields').dispatchEvent(event)
            specialitiesDataBox.innerHTML = ""
            specialityText.textContent = "Спецiальностi"
            specialityText.classList.add("default")


            $.ajax({
                type: 'GET',
                url: `specialities-data/${val}/`,
                success: function (response) {
                    const specialitiesData = response.data
                    specialitiesData.map(item => {
                        const option = document.createElement('div')
                        option.textContent = item.name
                        option.setAttribute('class', 'item')
                        option.setAttribute('data-value', item.name)
                        specialitiesDataBox.appendChild(option)
                    })
                    let val = document.querySelector("#specialities").getAttribute('data');
                    if (val !== '') {
                        document.querySelector("#specialities").setAttribute('data', '');
                        $('#specialities .default').html(val);
                    }
                },
                error: function (error) {
                    console.log(error)
                }
            })
        }
    },
    error: function (error) {
        console.log(error)
    }
})


fieldsInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedField = e.target.value

    specialitiesDataBox.innerHTML = ""
    specialityText.textContent = "Спецiальностi"
    specialityText.classList.add("default")


    $.ajax({
        type: 'GET',
        url: `specialities-data/${selectedField}/`,
        success: function(response){
            console.log(response.data)
            const specialitiesData = response.data
            specialitiesData.map(item=>{
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.name)
                specialitiesDataBox.appendChild(option)
            })
        },
        error: function(error){
            console.log(error)
        }
    })
})
