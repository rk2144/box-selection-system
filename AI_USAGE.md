# AI Usage

## 1. AI Tool Used

I used ChatGPT while working on this Django Box Selection System assignment.

## 2. How I Used AI

I asked questions about setting up a Django REST API, creating product and box models, implementing the box recommendation logic, writing tests, and uploading the project to GitHub.

## 3. Suggestions I Used

I used guidance about Django models, serializers, API endpoints, box dimensions, product rotation, weight validation, and automated testing.

## 4. Changes and Improvements

I reviewed the suggested code while integrating it into my project. I ran Django checks and tests and used the results to verify the implementation. Any additional changes should be listed here based on what I actually modified.

## 5. Issues and Limitations

The packing algorithm uses a heuristic to try different product orientations and placement positions. It does not guarantee finding every possible valid arrangement. I need to consider this limitation when evaluating the results.

## 6. Verification

I ran the following commands:

- `python manage.py check`
- `python manage.py test packaging`

My earlier test run reported 12 tests and an `OK` result. I will run the tests again after making further code changes and record the actual output.
