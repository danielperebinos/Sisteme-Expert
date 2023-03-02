BASE_URL = 'http://127.0.0.1:5000/';

ANIMALS_URL = function(){return BASE_URL + 'animals';};
TIPS_URL = function(animal){return BASE_URL + 'animals/' + animal + '/tips';};
EQUIPMENTS_URL = function(animal){return BASE_URL + 'animals/' + animal + '/equipments';};
DISEASES_URL = function(animal){return BASE_URL + 'animals/' + animal + '/diseases';};
SIMPTOMS_URL = function(animal){return BASE_URL + 'animals/' + animal + '/simptoms';};
DISEASE_SIMPTOMS_URL = function(animal, disease){return BASE_UR + 'animals/' + animal + '/' + disease + '/equipments';};

// console.log(ANIMALS_URL());
// console.log(TIPS_URL('dog'));
// console.log(EQUIPMENTS_URL('dog'));