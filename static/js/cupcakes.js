// Function to fetch cupcakes and add them to the page
function getCupcakes() {
    axios.get('/api/cupcakes')
        .then((response) => {
            const cupcakes = response.data.cupcakes;
            const cupcakeList = document.getElementById('cupcake-list');

            // Clear the existing list
            cupcakeList.innerHTML = '';

            // Populate the list with cupcakes
            cupcakes.forEach((cupcake) => {
                const li = document.createElement('li');
                li.textContent = `${cupcake.flavor} - Size: ${cupcake.size}, Rating: ${cupcake.rating}`;
                cupcakeList.appendChild(li);
            });
        })
        .catch((error) => {
            console.error('Error fetching cupcakes:', error);
        });
}

// Initial load: Get cupcakes and add to the page
function handleFormSubmit() {
    const form = document.getElementById('cupcake-form');
    const formData = new FormData(form);

    // Convert FormData to JSON
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    axios.post('/add-cupcake', JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json', // Set the content type to JSON
        },
    })
        .then(() => {
            // Clear form fields
            form.reset();

            // Refresh the list of cupcakes
            getCupcakes();
        })
        .catch((error) => {
            console.error('Error adding cupcake:', error);
        });
}

// Bind the form submission to the handleFormSubmit function
$('#cupcake-form').submit((event) => {
    event.preventDefault();
    handleFormSubmit();
});
