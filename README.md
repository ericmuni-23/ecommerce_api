This is a django project for running opperations of a ecommerce platform

# PROJECT DETAILS

This is a django project for running daily operations of an ecommerce platform

## API Documentation

This implementation provides the following endpoints:

### Product Search and Filtering:

**GET** /api/products/ - List all products with pagination

<br>
<br>

**Search**: /api/products/?search=keyword - Search in name, description, and category name

**Category filter**: /api/products/?category=1

**Price range**: /api/products/?min_price=10&max_price=100

**Stock availability**: /api/products/?in_stock=true

**Combined filters**: /api/products/?category=1&min_price=10&max_price=100&in_stock=true&search=keyword

### Individual Product View:

GET /api/products/{id}/ - Get detailed information about a specific product
