var updateButtons = document.getElementsByClassName('update-cart');
var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;


    for (var i = 0; i < updateButtons.length; i++) {
        updateButtons[i].addEventListener('click', function() {

            var productId = this.getAttribute('data-product');
            var action = this.getAttribute('data-action');

            fetch('../update_carrito/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken  // Agrega el token CSRF si es necesario
                },
                body: JSON.stringify({
                    'product_id': productId,
                    'action': action
                })
            })
            .then((response) => response.json())
            .then((data) => {
                // var cantidadElement = this.parentNode.querySelector('.cantidad');
                // cantidadElement.innerHTML = data.cantidad; 
                console.log('data:', data);
                location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }