
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
                    const cupcakeElement = $(`
                        <li>
                            Flavor: ${cupcake.flavor}<br>
                            Size: ${cupcake.size}<br>
                            Rating: ${cupcake.rating}<br>
                            Image: <img src="${cupcake.image}" alt="Cupcake Image"><br>
                            <button class="delete-cupcake" data-id="${cupcake.id}">Delete</button>
                            <button class="edit-cupcake" data-id="${cupcake.id}">Edit</button>
                        </li>`
                    );

                  
                    cupcakesList.append(cupcakeElement);

                    // Add click event handler for the delete button
                    cupcakeElement.find('.delete-cupcake').click(function () {
                        const cupcakeId = $(this).data('id');

                        // Call the deleteCupcake function with the cupcake ID
                        deleteCupcake(cupcakeId);
                    });

                    // Add click event handler for the edit button
                    cupcakeElement.find('.edit-cupcake').click(function () {
                        const cupcakeId = $(this).data('id');

                       
                        const newFlavor = prompt("Enter new flavor:", cupcake.flavor);
                        const newSize = prompt("Enter new size:", cupcake.size);
                        const newRating = parseFloat(prompt("Enter new rating:", cupcake.rating));
                        const newImage = prompt("Enter new image URL:", cupcake.image);

                        // Create an object with the updated cupcake data
                        const updatedCupcake = {
                            flavor: newFlavor,
                            size: newSize,
                            rating: newRating,
                            image: newImage || cupcake.image, // Use the original image if no new URL provided
                        };

                        // Send a PATCH request to update the cupcake
                        axios.patch(`/api/cupcakes/${cupcakeId}`, updatedCupcake)
                            .then(function () {
                                // Refresh the cupcakes list after updating
                                updateCupcakes();
                            })
                            .catch(function (error) {
                                console.error(`Error updating cupcake with ID ${cupcakeId}:`, error);
                            });
                    });
                });
            }
        })
        .catch(function (error) {
            console.error('Error fetching cupcakes:', error);
        });
}


function deleteCupcake(cupcakeId) {
   
    axios.delete(`/api/cupcakes/${cupcakeId}`)
        .then(function () {
          
            updateCupcakes();
        })
        .catch(function (error) {
            console.error(`Error deleting cupcake with ID ${cupcakeId}:`, error);
        });
}


$(document).ready(function () {
    // Initial fetch and page update
    updateCupcakes();

   
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
             
                $('#flavor').val('');
                $('#size').val('');
                $('#rating').val('');
                $('#image').val('');

          
                updateCupcakes();
            })
            .catch(function (error) {
                console.error('Error adding cupcake:', error);
            });
    });
});
