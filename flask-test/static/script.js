const form = document.getElementById('ml-form');
const genderButtons = document.querySelectorAll('.gender-dropdown-content span');
const genderInput = document.querySelector('#gender-input');
const civilStatusButtons = document.querySelectorAll('.civil-status-dropdown-content span');
const civilStatusInput = document.querySelector('#civil-status-input');
const predictionElement = document.getElementById('prediction');
const resultsElement = document.getElementById('results');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    formData.set('genero', genderInput.value);
    formData.set('estado_civil', civilStatusInput.value);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        predictionElement.textContent = data.prediction;
        resultsElement.style.display = 'block';
    })
    .catch(error => console.error(error));
});

genderButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        genderInput.value = button.getAttribute('value');
        document.querySelector('.gender-dropbtn').value = button.textContent;
    });
});

civilStatusButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        civilStatusInput.value = button.getAttribute('value');
        document.querySelector('.civil-status-dropbtn').value = button.textContent;
    });
});
