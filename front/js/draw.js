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
                options += `<option value=${element}>${element}</option>`
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
                    <input type="checkbox" name="${element}">
                    <label for="${element}">${element}</label><br>`
            });
            $('#diseases').html(diseases);
        }
    );    
}

function generalAnimal(form){
    console.log(form);
}

addAnimalOptions();