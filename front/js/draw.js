function tipsFormAction(){
    animal = $('#animals').find(":selected").val();
    console.log(animal);
    if(animal){
        drawAnimalTips(animal);
    }
}

function addAnimalOptions(){
    get_animals().then(
        (response) => {
            let options = '<option selected>Select animal</option>'; 
            response.forEach(element => {
                options += `<option value=${element}>${element}</option>`;
            });

            $('#animals').html(options);
        }
    )
}

function drawAnimalTips(animal){
    get_tips(animal).then(
        (response) => {
            let tips = '';
            response.forEach(element => {
                tips += `
                    <div class="card mb-5">
                        <div class="card-title">${element.Short}</div>
                        <div class="card-body">${element.Long}</div>
                    </div>`
            });
            $('#tips').html(tips);
        }
    )    
}

function drawAnimalSimptoms(){
    animal = $('#animals').find(":selected").val();
    console.log(animal);
    get_simptoms(animal).then(
        (response) => {
            let diseases = '';
            response.forEach(element => {
                diseases += `
                    <input class="simptomsbox" type="checkbox" value="${element}" name="${element}">
                    <label for="${element}">${element}</label><br>`
            });
            $('#diseases').html(diseases);
        }
    );    
}

function drawAnimalDiseasesBySimptoms(){
    animal = $('#animals').find(":selected").val();

    values = [];
    $('.simptomsbox:checked').each(function(i) {
        values[i] = $(this).val();
    });
    
    get_diseases_by_simptoms(animal, values).then(
        (response) => {
            scores = Object.keys(response.score);
            const sum = Object.values(response.score).reduce((partialSum, a) => partialSum + a, 0); 
            scores.sort(function(a, b){return response.score[b]- response.score[a]})
            
            let diseases = ``;

            scores.forEach(element => {
                diseases += `
                    <div class="card mb-5">
                        <div class="card-title">${(response.score[element]/sum).toFixed(2)*100}% <b>${element}</b></div>
                        <div class="card-body">
                        <i>Simptoms: </i>
                        <ul class="list-group list-group-flush">
                `;

                response.diseases_simptoms[element].forEach(simptom => {
                    diseases += `<li class="list-group-item">${simptom}</li>`;
                });

                diseases += `</ul></div></div>`;
            });

            $('#simptoms_from_bd').html(diseases);
        }
    )
}

function drawAnimalDiseases(form){
    animal = $('#animals').find(":selected").val();
    
    let diseases = '';

    get_diseases(animal).then(
        (response) => {
            response.diseases.forEach(element => {
                diseases += `
                    <div class="card mb-5">
                        <div class="card-title"><b>${element.Disease}</b></div>
                        <div class="card-body">
                            <i>Description: </i> <br>
                            ${element.Description}
                        </div>
                    </div>
                `;
            });

            $('#diseases').html(diseases);
        }
    )
}

addAnimalOptions();