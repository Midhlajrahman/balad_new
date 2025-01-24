document.addEventListener("DOMContentLoaded", function () {
    // Get all category links
    const categoryLinks = document.querySelectorAll('.category-list a');

    // Get all product items
    const products = document.querySelectorAll('.product-list .card-product');

    // Add click event to each category link
    categoryLinks.forEach(link => {
        link.addEventListener('click', function () {
            // Get the selected category from the data-category attribute
            const selectedCategory = this.getAttribute('data-category');

            // Filter products based on selected category
            filterProductsByCategory(selectedCategory);

            // Optionally, highlight the active category
            categoryLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Function to filter products based on category
    function filterProductsByCategory(categorySlug) {
        products.forEach(product => {
            const productCategory = product.getAttribute('data-category');

            if (categorySlug === 'all' || productCategory === categorySlug) {
                // Show product if category matches or 'all' is selected
                product.style.display = 'block';
            } else {
                // Hide product if category doesn't match
                product.style.display = 'none';
            }
        });
    }

    // Optionally, trigger filter based on default category on page load
    const defaultCategory = document.querySelector('.category-list a.active');
    if (defaultCategory) {
        filterProductsByCategory(defaultCategory.getAttribute('data-category'));
    }
});

document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();

        // Update the button text to the selected filter
        const selectedFilter = event.target.getAttribute('data-value');
        const button = document.getElementById('dropdownMenuButton');
        button.textContent = event.target.textContent;

        // Get both product containers for each tab
        const productsContainers = document.querySelectorAll('.product-list');

        productsContainers.forEach(productsContainer => {
            const products = Array.from(productsContainer.getElementsByClassName('card-product'));

            let sortedProducts;
            if (selectedFilter === "latest") {
                sortedProducts = products.sort((a, b) => parseInt(b.dataset.item) - parseInt(a.dataset.item));
            } else if (selectedFilter === "low-to-high") {
                sortedProducts = products.sort((a, b) => parseFloat(a.dataset.price) - parseFloat(b.dataset.price));
            } else if (selectedFilter === "high-to-low") {
                sortedProducts = products.sort((a, b) => parseFloat(b.dataset.price) - parseFloat(a.dataset.price));
            }


            // Clear the container and append sorted products
            productsContainer.innerHTML = "";
            sortedProducts.forEach(product => productsContainer.appendChild(product));
        });
    });
});

const uniqueColors = new Set();
const colorItems = document.querySelectorAll('.list-color-item1');

colorItems.forEach(item => {
    const swatchValue = item.querySelector('.swatch-value1');
    const colorHex = swatchValue ? swatchValue.style.backgroundColor.trim() : null;

    // Check if the color already exists in the set
    if (colorHex && !uniqueColors.has(colorHex)) {
        uniqueColors.add(colorHex); // Add the unique color
    } else {
        // Hide duplicate color items
        item.style.display = "none";
    }
});

document.querySelectorAll('.list-color-item').forEach(item => {
    item.addEventListener('click', () => {
        const selectedColor = item.querySelector('.swatch-value').getAttribute('data-color').trim();

        if (!selectedColor) return; // Exit if no color is selected

        // Get all product cards
        const productCards = document.querySelectorAll('.card-product');

        productCards.forEach(card => {
            const productColors = card.getAttribute('data-color').split(' ');

            // Show or hide products based on color match
            if (productColors.includes(selectedColor)) {
                card.style.display = "block"; // Show the product
            } else {
                card.style.display = "none"; // Hide the product
            }
        });

        // Update active state for color selection
        document.querySelectorAll('.list-color-item').forEach(swatch => swatch.classList.remove('active'));
        item.classList.add('active');
    });
});

document.querySelectorAll('.list-brand-item').forEach(item => {
    item.addEventListener('click', () => {
        const selectedBrand = item.querySelector('.brand-name').textContent.trim();

        if (!selectedBrand) return; // Exit if no brand is selected

        // Get all product cards
        const productCards = document.querySelectorAll('.card-product');

        productCards.forEach(card => {
            // Get the brand(s) associated with the product
            const productBrands = card.getAttribute('data-brand').split(' ');

            // Show or hide products based on brand match
            if (productBrands.includes(selectedBrand)) {
                card.style.display = "block"; // Show the product
            } else {
                card.style.display = "none"; // Hide the product
            }
        });

        // Update active state for brand selection
        document.querySelectorAll('.list-brand-item').forEach(brand => brand.classList.remove('active'));
        item.classList.add('active');
    });
});

$(document).ready(function () {

    // Handle price range slider
    $(".price-range-slider").on("input", function () {
        let minPrice = parseFloat($(this).val());
        let maxPrice = parseFloat($(this).attr("max"));

        // Update price display
        $("#min-price").text(minPrice.toFixed(2));
        $("#max-price").text(maxPrice.toFixed(2));

        // Filter products based on price range
        filterProducts(minPrice, maxPrice);
    });

    // Function to filter products based on category and price range
    function filterProducts(minPrice = 0, maxPrice = 2000) {
        $(".isotope-item").each(function () {
            let productPrice = parseFloat($(this).data("price"));

            // Check if the product's price falls within the selected price range
            let showPrice = productPrice >= minPrice && productPrice <= maxPrice;

            // Show the product if both category and price match
            if (showPrice) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    // Function to handle size change
    function handleSizeChange(event) {
        const selectedSize = event.target;
        const productId = selectedSize.getAttribute('data-product-id');
        const salePrice = selectedSize.getAttribute('data-sale-price');
        const regularPrice = selectedSize.getAttribute('data-regular-price');
        const salePriceElement = document.querySelector(`#price-on-sale-${productId}`);
        const regularPriceElement = document.querySelector(`#compare-at-price-${productId}`);
        const priceElement = document.querySelector(`#tf-qty-price-${productId}`);
        const sizeLabel = document.querySelector(`#current-size-${productId}`);

        // Ensure elements exist before attempting to update them
        if (salePriceElement) {
            salePriceElement.innerText = salePrice;
        } else {
            console.error(`Element with ID price-on-sale-${productId} not found.`);
        }

        if (regularPriceElement) {
            regularPriceElement.innerText = regularPrice;
        } else {
            console.error(`Element with ID compare-at-price-${productId} not found.`);
        }

        if (sizeLabel) {
            sizeLabel.innerText = selectedSize.nextElementSibling.innerText.trim();
        } else {
            console.error(`Element with ID current-size-${productId} not found.`);
        }

        if (priceElement) {
            priceElement.innerText = `$${salePrice}`;
        } else {
            console.error(`Element with ID tf-qty-price-${productId} not found.`);
        }
    }

    // Attach event listeners to modal show event
    const modals = document.querySelectorAll('.modalDemo');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function () {
            const productId = modal.getAttribute('id').split('_').pop();
            const sizeSelectors = modal.querySelectorAll(`.size-selector[name="product_size-${productId}"]`);

            sizeSelectors.forEach(selector => {
                selector.addEventListener('change', handleSizeChange);
            });
        });
    });

    // Handle add to cart button click
    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const productId = this.getAttribute('data-product');
            const quantity = this.closest('.modal-content').querySelector('.quantity__input').value;
            const price = this.querySelector('.tf-qty-price').innerText;

            // Handle the add to cart logic here
            console.log(`Adding product ID: ${productId} to cart with quantity: ${quantity} and price: ${price}`);


        });
    });
});

