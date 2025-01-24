

// $(document).ready(function () {
//     // Function to update prices and offer percent for a specific card
//     function updatePricesAndOffer(card) {
//         var selectedRadio = card.find('input[name="product_size"]:checked');
//         if (selectedRadio.length > 0) {
//             var salePrice = selectedRadio.data('sale_price');
//             var originalPrice = selectedRadio.data('original_price');
//             var offerPercent = parseFloat(selectedRadio.data('offer_percent')).toFixed(2);

//             card.find('.sale_price').text('₹' + salePrice);
//             card.find('.original_price').text('₹' + originalPrice);
//             card.find('.offer_percent').text(offerPercent + '% OFF');
//         }
//     }

//     // Attach event listener for radio button clicks
//     $('input[name="product_size"]').off('click').on('click', function () {
//         var card = $(this).closest('.cart-div');
//         updatePricesAndOffer(card);
//     });

//     // Function to handle quantity changes
//     function handleQuantityChange(change) {
//         var inputField = $(".quantity__input");
//         var currentQuantity = parseInt(inputField.val(), 10);

//         // Default to 0 if the current value is not a number
//         if (isNaN(currentQuantity)) {
//             currentQuantity = 0;
//         }

//         // Calculate the new quantity
//         var newQuantity = currentQuantity + change;

//         // Ensure the new quantity is at least 0
//         newQuantity = Math.max(0, newQuantity);

//         // Update the input field value
//         inputField.val(newQuantity);

//         var addToCartButton = $("#cart-add-btn");
//         addToCartButton.prop("disabled", newQuantity === 0);
//     }

//     // Attach event listeners for quantity changes
//     $(".quantity__plus").off("click").on("click", function () {
//         handleQuantityChange(1);
//     });

//     $(".quantity__minus").off("click").on("click", function () {
//         handleQuantityChange(-1);
//     });

//     // Attach event listener for Add to Cart button click
//     $(".cart-add-btn").off("click").on("click", function () {
//         var product_Id = $('input[name="product_size"]:checked').val();
//         var quantity = $("input[name='quantity']").val();
//         var url = "/shop/cart/add/?product_id=" + product_Id + "&quantity=" + quantity;
//         console.log(url)
//         $.ajax({
//             type: "GET",
//             url: url,
//             success: function (data) {
//                 $('.header_cart_count').html(data.cart_count);
//                 Swal.fire({
//                     title: "<strong>Item Added to Cart</strong>",
//                     icon: "success",
//                     html: `
//                         <p>Your item has been added to the cart successfully!</p>
//                         <p>What would you like to do next?</p>
//                     `,
//                     showCloseButton: true,
//                     showCancelButton: true,
//                     focusConfirm: false,
//                     confirmButtonText: `
//                         View Cart
//                         <i class="fa fa-shopping-cart"></i>
//                     `,
//                     confirmButtonAriaLabel: "View Cart",
//                     cancelButtonText: `
//                         Checkout
//                         <i class="fa fa-credit-card"></i>
//                     `,
//                     cancelButtonAriaLabel: "Checkout",
//                     timer: 5000,
//                     timerProgressBar: true
//                 }).then((result) => {
//                     if (result.isConfirmed) {
//                         window.location.href = '/shop/cart/';
//                     } else if (result.dismiss === Swal.DismissReason.cancel) {
//                         window.location.href = '/checkout/';
//                     }
//                 });
//             },
//             error: function (data) {
//                 if (data.status == '401') {
//                     window.location.href = '/accounts/login/';
//                 } else {
//                     Swal.fire({
//                         title: "Error",
//                         icon: "error",
//                         text: data.responseJSON.message || "An error occurred while adding the item to the cart."
//                     });
//                 }
//             }
//         });
//     });

//     // Attach event listener for Add to Wishlist button click
//     $(".wishlist-btn").off("click").on("click", function () {
//         var product = $(this).data('product');
//         var url = "/wishlist/add/?product_id=" + product;

//         $.ajax({
//             type: "GET",
//             url: url,
//             success: function (data) {
//                 Swal.fire({
//                     title: "<strong>Item Added to Wishlist</strong>",
//                     icon: "success",
//                     html: `
//                         <p>Your item has been added to your wishlist successfully!</p>
//                         <p>What would you like to do next?</p>
//                     `,
//                     showCloseButton: true,
//                     showCancelButton: true,
//                     focusConfirm: false,
//                     confirmButtonText: `
//                         View Wishlist
//                         <i class="fa fa-heart"></i>
//                     `,
//                     confirmButtonAriaLabel: "View Wishlist",
//                     cancelButtonText: `
//                         Continue Shopping
//                         <i class="fa fa-shopping-bag"></i>
//                     `,
//                     cancelButtonAriaLabel: "Continue Shopping",
//                     timer: 5000,
//                     timerProgressBar: true
//                 }).then((result) => {
//                     if (result.isConfirmed) {
//                         window.location.href = '/wishlist';
//                     } else if (result.dismiss === Swal.DismissReason.cancel) {
//                         window.location.href = '/shop';
//                     }
//                 });
//             },
//             error: function (data) {
//                 if (data.status == '401') {
//                     window.location.href = '/accounts/login/';
//                 } else {
//                     Swal.fire({
//                         title: "Error",
//                         icon: "error",
//                         text: data.responseJSON.message || "An error occurred while adding the item to the wishlist."
//                     });
//                 }
//             }
//         });
//     });
// });



// #working

// $(document).ready(function () {
//     // Function to update prices and offer percent for a specific card
//     function updatePricesAndOffer(card) {
//         var selectedRadio = card.find('input[name^="product_size-"]:checked');
//         if (selectedRadio.length > 0) {
//             var salePrice = selectedRadio.data('sale_price');
//             var originalPrice = selectedRadio.data('original_price');
//             var offerPercent = parseFloat(selectedRadio.data('offer_percent')).toFixed(2);

//             card.find('.sale_price').text('₹' + salePrice);
//             card.find('.original_price').text('₹' + originalPrice);
//             card.find('.offer_percent').text(offerPercent + '% OFF');
//         }
//     }

//     // Attach event listener for radio button clicks
//     $('input[name^="product_size-"]').off('click').on('click', function () {
//         var card = $(this).closest('.cart-div');
//         updatePricesAndOffer(card);
//     });

//     // Function to handle quantity changes
//     function handleQuantityChange(change) {
//         var inputField = $(".quantity__input");
//         var currentQuantity = parseInt(inputField.val(), 10);

//         // Default to 0 if the current value is not a number
//         if (isNaN(currentQuantity)) {
//             currentQuantity = 0;
//         }

//         // Calculate the new quantity
//         var newQuantity = currentQuantity + change;

//         // Ensure the new quantity is at least 0
//         newQuantity = Math.max(0, newQuantity);

//         // Update the input field value
//         inputField.val(newQuantity);

//         var addToCartButton = $("#cart-add-btn");
//         addToCartButton.prop("disabled", newQuantity === 0);
//     }

//     // Attach event listeners for quantity changes
//     $(".quantity__plus").off("click").on("click", function () {
//         handleQuantityChange(1);
//     });

//     $(".quantity__minus").off("click").on("click", function () {
//         handleQuantityChange(-1);
//     });

//     // Attach event listener for Add to Cart button click
//     $(".cart-add-btn").off("click").on("click", function () {
//         var productId = $(this).data('product');
//         var selectedRadio = $(`input[name="product_size-${productId}"]:checked`);

//         // Check if a product size is selected
//         if (selectedRadio.length === 0) {
//             Swal.fire({
//                 title: "Error",
//                 icon: "error",
//                 text: "Please select a product size."
//             });
//             return;
//         }

//         var quantity = $(this).closest('.modal-content').find("input[name='quantity']").val();
//         var url = `/shop/cart/add/?product_id=${selectedRadio.val()}&quantity=${quantity}`;

//         console.log(url);

//         $.ajax({
//             type: "GET",
//             url: url,
//             success: function (data) {
//                 $('.header_cart_count').html(data.cart_count);
//                 Swal.fire({
//                     title: "<strong>Item Added to Cart</strong>",
//                     icon: "success",
//                     html: `
//                         <p>Your item has been added to the cart successfully!</p>
//                         <p>What would you like to do next?</p>
//                     `,
//                     showCloseButton: true,
//                     showCancelButton: true,
//                     focusConfirm: false,
//                     confirmButtonText: `
//                         View Cart
//                         <i class="fa fa-shopping-cart"></i>
//                     `,
//                     confirmButtonAriaLabel: "View Cart",
//                     cancelButtonText: `
//                         Checkout
//                         <i class="fa fa-credit-card"></i>
//                     `,
//                     cancelButtonAriaLabel: "Checkout",
//                     timer: 5000,
//                     timerProgressBar: true
//                 }).then((result) => {
//                     if (result.isConfirmed) {
//                         window.location.href = '/shop/cart/';
//                     } else if (result.dismiss === Swal.DismissReason.cancel) {
//                         window.location.href = '/checkout/';
//                     }
//                 });
//             },
//             error: function (data) {
//                 if (data.status == '401') {
//                     window.location.href = '/accounts/login/';
//                 } else {
//                     Swal.fire({
//                         title: "Error",
//                         icon: "error",
//                         text: data.responseJSON.message || "An error occurred while adding the item to the cart."
//                     });
//                 }
//             }
//         });
//     });
// });







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
        var url = `/shop/cart/add/?product_id=${selectedRadio.val()}&quantity=${quantity}`;

        console.log(url);

        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('.header_cart_count').html(data.cart_count);

        // Display the custom modal
        $('#shoppingCart').modal('show');

        // Update the modal content with cart items
        $('#shoppingCart .modal-body .cart-items').html(data.cart_items_html);
            },
            error: function (data) {
                if (data.status == '401') {
                    window.location.href = '/accounts/login/';
                } else {
                    Swal.fire({
                        title: "Error",
                        icon: "error",
                        text: data.responseJSON.message || "An error occurred while adding the item to the cart."
                    });
                }
            }
        });
    });
});