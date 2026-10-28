# Box Selection System

A Django REST API that recommends a suitable shipping box for an ecommerce order based on product dimensions, total weight, box capacity, and box cost.

## Project Overview

When a customer places an order, the warehouse needs to select a shipping box that can accommodate all the ordered products without exceeding the box's maximum weight capacity.

This project uses Django and Django REST Framework to manage products and boxes and recommend the lowest-cost suitable box.

## Features

- Create and list products.
- Create and list shipping boxes.
- Store product dimensions and weight.
- Store box internal dimensions, maximum weight capacity, and cost.
- Support multiple products and quantities in an order.
- Check product rotation and placement inside a box.
- Reject boxes that exceed the order's total weight.
- Recommend the lowest-cost feasible box.
- Return an error when no suitable box is found.
- Validate product dimensions, box dimensions, and order quantities.
- Automated tests using Django's testing framework.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- Git and GitHub

## Project Structure

```text
box-selection-system/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── packaging/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── admin.py
├── manage.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
└── TEST_OUTPUT.md
```

## Requirements

- Python 3.10 or later
- pip
- Git

Use a Python version supported by your installed Django version.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/rk2144/box-selection-system.git
cd box-selection-system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Run Django checks

```bash
python manage.py check
```

### 6. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products/` | List products |
| POST | `/api/products/` | Create a product |
| GET | `/api/boxes/` | List shipping boxes |
| POST | `/api/boxes/` | Create a shipping box |
| POST | `/api/recommend-box/` | Recommend a box for an order |

### Create a Product

Send a POST request to `/api/products/` with JSON:

```json
{
  "name": "Laptop",
  "length": "10.00",
  "width": "8.00",
  "height": "4.00",
  "weight": "2.000"
}
```

Dimensions are measured in centimetres and weight in kilograms.

### Create a Shipping Box

Send a POST request to `/api/boxes/`:

```json
{
  "name": "Small Box",
  "inner_length": "12.00",
  "inner_width": "10.00",
  "inner_height": "6.00",
  "max_weight": "5.000",
  "cost": "20.00"
}
```

Box cost is stored as a decimal monetary value. The project currently uses the cost value provided in the database.

### Recommend a Box

Send a POST request to `/api/recommend-box/`:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ]
}
```

The product ID must refer to a product that exists in the database.

Example successful response:

```json
{
  "box_id": 1,
  "box_name": "Small Box",
  "cost": "20.00",
  "total_weight": "2.000"
}
```

The response values above are illustrative; the actual result depends on the stored data and packing feasibility.

If no suitable box is found, the API returns a `404 Not Found` response with a message explaining that no suitable box was found.

Invalid request data or nonexistent product IDs return a `400 Bad Request` response.

## Box Selection Algorithm

The selection process follows these steps:

1. Validate the order items and quantities.
2. Calculate the total order weight.
3. Expand product quantities into individual items.
4. Reject boxes whose maximum weight capacity is insufficient.
5. Consider the six possible orientations of each rectangular product.
6. Attempt to place each product inside the box without exceeding its internal dimensions or overlapping previously placed products.
7. Select the feasible box with the lowest cost.
8. Return no suitable box if no candidate passes the checks.

When two suitable boxes have the same cost, the implementation uses the box's database primary key as a tie-breaker.

### Algorithm Limitations

The current packing implementation uses a greedy heuristic with a limited set of candidate placement coordinates. It is not an exhaustive 3D packing solver.

Consequently, it may fail to find a valid arrangement even when another arrangement exists. It assumes rectangular products, axis-aligned placement, and freely permitted rotation. It does not account for packaging material thickness, fragile items, stacking restrictions, or extra clearance.

## Running Tests

Run the application tests with:

```bash
python manage.py test packaging
```

The test suite covers packing feasibility, rotation, weight capacity, cheapest-box selection, invalid quantities, empty orders, and API validation.

Refer to `TEST_OUTPUT.md` for the actual test output included with the submission.

## Django Admin

To manage products and boxes through the Django Admin interface:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

## AI Usage

AI tools were used during development assistance. See `AI_USAGE.md` for the actual prompts, accepted suggestions, modifications, identified mistakes, and verification steps.

## Author

Rinku Lodhi

## License

No license has been specified for this project.
