async function get_animals(){
    let reponse = await fetch(ANIMALS_URL);
    if (reponse.status == 200){
        let json = await reponse.json();
        return json.animals;
    }
    return [];
}