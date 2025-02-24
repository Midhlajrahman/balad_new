
$(document).ready(function () {
    // Function to update prices and offer percent for a specific card
    function updatePricesAndOffer(card) {
        var selectedRadio = card.find('input[name^="product_size-"]:checked');
        if (selectedRadio.length > 0) {
            var salePrice = selectedRadio.data('sale_price');
            var originalPrice = selectedRadio.data('original_price');
            var offerPercent = parseFloat(selectedRadio.data('offer_percent')).toFixed(2);

            card.find('.sale_price').text('₹' + salePrice);
            card.find('.original_price').text('₹' + originalPrice);
            card.find('.offer_percent').text(offerPercent + '% OFF');
        }
    }

    // Attach event listener for radio button clicks
    $('input[name^="product_size-"]').off('click').on('click', function () {
        var card = $(this).closest('.cart-div');
        updatePricesAndOffer(card);
    });

    // Function to handle quantity changes
    function handleQuantityChange(change) {
        var inputField = $(".quantity__input");
        var currentQuantity = parseInt(inputField.val(), 10);

        // Default to 0 if the current value is not a number
        if (isNaN(currentQuantity)) {
            currentQuantity = 0;
        }

        // Calculate the new quantity
        var newQuantity = currentQuantity + change;

        // Ensure the new quantity is at least 0
        newQuantity = Math.max(0, newQuantity);

        // Update the input field value
        inputField.val(newQuantity);

        var addToCartButton = $("#cart-add-btn");
        addToCartButton.prop("disabled", newQuantity === 0);
    }

    // Attach event listeners for quantity changes
    $(".quantity__plus").off("click").on("click", function () {
        handleQuantityChange(1);
    });

    $(".quantity__minus").off("click").on("click", function () {
        handleQuantityChange(-1);
    });

    // Attach event listener for Add to Cart button click
    // $(".cart-add-btn").off("click").on("click", function () {
    //     var productId = $(this).data('product');
    //     var selectedRadio = $(`input[name="product_size-${productId}"]:checked`);

    //     // Check if a product size is selected
    //     if (selectedRadio.length === 0) {
    //         Swal.fire({
    //             title: "Error",
    //             icon: "error",
    //             text: "Please select a product size."
    //         });
    //         return;
    //     }

    //     var quantity = $(this).closest('.modal-content').find("input[name='quantity']").val();
    //     var url = `/shop/cart/add/?product_id=${selectedRadio.val()}&quantity=${quantity}`;

    //     console.log(url);

    //     $.ajax({
    //         type: "GET",
    //         url: url,
    //         success: function (data) {
           
    //             $('.header_cart_count').html(data.cart_count);

    //     // Display the custom modal
    //     $('#shoppingCart').modal('show');

    //     // Update the modal content with cart items
    //     $('#shoppingCart .modal-body .cart-items').html(data.cart_items_html);
    //         },
    //         error: function (data) {
    //             if (data.status == '401') {
    //                 window.location.href = '/accounts/login/';
    //             } else {
    //                 Swal.fire({
    //                     title: "Error",
    //                     icon: "error",
    //                     text: data.responseJSON.message || "An error occurred while adding the item to the cart."
    //                 });
    //             }
    //         }
    //     });
    // });

    // $(".cart-add-btn").off("click").on("click", function () {
        
    //     var productId = $(this).data('product');
    //     var selectedRadio = $(`input[name="product_size-${productId}"]:checked`);
    
    //     // Check if a product size is selected
    //     if (selectedRadio.length === 0) {
    //         Swal.fire({
    //             title: "Error",
    //             icon: "error",
    //             text: "Please select a product size."
    //         });
    //         return;
    //     }
    
    //     var quantity = $(this).closest('.modal-content').find("input[name='quantity']").val();
    //     var url = `/shop/cart/add/?product_id=${selectedRadio.val()}&quantity=${quantity}`;
    
    //     console.log(url);
    
    //     $.ajax({
    //         type: "GET",
    //         url: url,
    //         success: function (data) {
    //             console.log(data.cart_modal_html)
    //             // Update the cart count in the header
    //             $('.header_cart_count').html(data.cart_count);
    
    //             // Display the custom modal
    //             // $('#shoppingCart').modal('show');
             
    
    //             // Update the modal content with cart items
    //             if (data.cart_modal_html) {
    //                 $('#shoppingCart .modal-body .cart-items').html(data.cart_modal_html);
    //             } else {
    //                 console.error("Cart items HTML is missing from the response.");
    //             }
               

    //             $('#shoppingCart').modal('show');
    //         },
    //         error: function (data) {
    //             if (data.status == '401') {
    //                 window.location.href = '/accounts/login/';
    //             } else {
    //                 Swal.fire({
    //                     title: "Error",
    //                     icon: "error",
    //                     text: data.responseJSON.message || "An error occurred while adding the item to the cart."
    //                 });
    //             }
    //         }
    //     });
   
    // });



    $(document).ready(function () {
        // Check if the flag is set in localStorage
        if (localStorage.getItem('showCartModal') === 'true') {
            // Show the modal
            $('#shoppingCart').modal('show');
            // Clear the flag
            localStorage.removeItem('showCartModal');
        }
    });

    $(".cart-add-btn").off("click").on("click", function () {
        var productId = $(this).data('product');
        var selectedRadio = $(`input[name="product_size-${productId}"]:checked`);
        
        // Check if a product size is selected
        if (selectedRadio.length === 0) {
            Swal.fire({
                title: "Error",
                icon: "error",
                text: "Please select a product size."
            });
            return;
        }
        
        var quantity = $(this).closest('.modal-content').find("input[name='quantity']").val();
        var url = `/shop/cart/add/?product_id=${selectedRadio.val()}&quantityy=${quantity}`;
        
        console.log(url);
        
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                console.log(data.cart_modal_html);
                // Update the cart count in the header
                $('.header_cart_count').html(data.cart_count);
                
                // Update the modal content with cart items
                if (data.cart_modal_html) {
                    $('#shoppingCart .modal-body .cart-items').html(data.cart_modal_html);
                } else {
                    console.error("Cart items HTML is missing from the response.");
                }

                // Set the flag in localStorage
                localStorage.setItem('showCartModal', 'true');

                // Reload the page
                location.reload();
            }
        });
    });

});