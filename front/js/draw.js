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

addAnimalOptions();