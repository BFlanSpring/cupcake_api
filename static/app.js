// Wait for the DOM to be ready
$(document).ready(function () {
    // Function to fetch cupcakes from the API and update the page
    function updateCupcakes() {
        axios.get('/api/cupcakes')
            .then(function (response) {
                const cupcakes = response.data.cupcakes;
                const cupcakesList = $('#cupcakes-list');
                cupcakesList.empty();

                if (cupcakes.length === 0) {
                    cupcakesList.append('<li>No cupcakes found.</li>');
                } else {
                    cupcakes.forEach(function (cupcake) {
                        cupcakesList.append(
                            `<li>
                                Flavor: ${cupcake.flavor}<br>
                                Size: ${cupcake.size}<br>
                                Rating: ${cupcake.rating}<br>
                                Image: <img src="${cupcake.image}" alt="Cupcake Image"><br>
                            </li>`
                        );
                    });
                }
            })
            .catch(function (error) {
                console.error('Error fetching cupcakes:', error);
            });
    }

    // Initial fetch and page update
    updateCupcakes();

    // Handle form submission
    $('#cupcake-form').submit(function (event) {
        event.preventDefault();

        const formData = {
            flavor: $('#flavor').val(),
            size: $('#size').val(),
            rating: parseFloat($('#rating').val()),
            image: $('#image').val()
        };

        axios.post('/api/cupcakes/new', formData)
            .then(function () {
                // Clear the form
                $('#flavor').val('');
                $('#size').val('');
                $('#rating').val('');
                $('#image').val('');

                // Fetch and update cupcakes
                updateCupcakes();
            })
            .catch(function (error) {
                console.error('Error adding cupcake:', error);
            });
    });
});
