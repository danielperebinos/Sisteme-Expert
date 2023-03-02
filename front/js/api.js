async function get_animals(){
    let reponse = await fetch(ANIMALS_URL());
    if (reponse.status == 200){
        let json = await reponse.json();
        return json.animals;
    }
    return [];
}

async function get_tips(animal){
    console.log(TIPS_URL(animal));
    let reponse = await fetch(TIPS_URL(animal));
    if (reponse.status == 200){
        let json = await reponse.json();
        return json.tips;
    }
    return [];
}

async function get_equipments(animal){
    let reponse = await fetch(EQUIPMENTS_URL(animal));
    if (reponse.status == 200){
        let json = await reponse.json();
        return json.equipments;
    }
    return [];
}

async function get_simptoms(animal){
    let reponse = await fetch(SIMPTOMS_URL(animal));
    if (reponse.status == 200){
        let json = await reponse.json();
        return json.simptoms;
    }
    return [];
}

async function get_simptoms(animal){
    let reponse = await fetch(SIMPTOMS_URL(animal));
    if (reponse.status == 200){
        let json = await reponse.json();
        return json.simptoms;
    }
    return [];
}

async function get_disease_simptoms(animal, disease){
    let reponse = await fetch(DISEASE_SIMPTOMS_URL(animal, disease));
    if (reponse.status == 200){
        let json = await reponse.json();
        return json.simptoms;
    }
    return [];
}