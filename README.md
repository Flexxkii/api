## FastAPI Data Retrieval and Sorting

This Python code provides an API endpoint using FastAPI to retrieve and sort property data from a simulated data source. The API supports filtering and sorting based on various parameters. Here's a detailed explanation of the code and how to use the API:

### API Endpoints

#### 1. **`/get_all_data`**
   - **Description:** Retrieve all property data, optionally sorted and filtered.
   - **Parameters:**
     - None
   - **Response:**
     - `data`: List of property objects sorted and filtered based on parameters.
   - **Example Request:**
     ```http
     GET /get_all_data
     ```
  
#### 2. **`/data`**
   - **Description:** Retrieve filtered and sorted property data based on query parameters.
   - **Parameters:**
     - `city` (optional): Filter data by city.
     - `min_price` (optional): Filter data by minimum price.
     - `max_price` (optional): Filter data by maximum price.
     - `bedrooms` (optional): Filter data by number of bedrooms.
     - `sort` (optional): Sort data by 'price_asc', 'price_desc', 'date_new', or 'date_old'.
     - `return_city_only` (optional): If true, return only the city names of the filtered data.
   - **Response:**
     - List of filtered and sorted property objects or city names.
   - **Example Request:**
     ```http
     GET /data?city=New York&min_price=100000&max_price=500000&bedrooms=2&sort=price_asc&return_city_only=true
     ```

### Code Structure

1. **Imports:**
   - FastAPI is used for creating the API endpoints.
   - `time` and `psutil` modules are used for measuring execution time and CPU usage.
   - `httpx` is used for making asynchronous HTTP requests.
   - `json` module is used for JSON file operations.

2. **Global Async Client:**
   - An asynchronous HTTP client is created using `httpx.AsyncClient()` for efficient data fetching.

3. **Data Fetching:**
   - Data is fetched in chunks using an asynchronous generator function `fetch_data_in_chunks(cursor=0)`. It fetches data from a remote API endpoint and yields results in chunks.

4. **Data Sorting:**
   - Data is sorted based on the provided sorting parameter using the `sort_data(data, sort_param)` function.

5. **API Endpoints:**
   - `/get_all_data`: Retrieves all property data, measures execution time, and CPU usage. Returns sorted and filtered data.
   - `/data`: Retrieves filtered and sorted property data based on query parameters. Handles filtering, sorting, and optional city-only response.

### Usage Guidelines

1. Ensure FastAPI and required modules are installed (`fastapi`, `httpx`, `psutil`).
2. Run the FastAPI application using a web server (`uvicorn main:app --reload` assuming the code is in `main.py`).
3. Access the API endpoints as described above using appropriate HTTP requests.

## Data Processing Script Documentation

The provided Python script performs various operations on fetched data from a remote API endpoint. It processes the data, groups specific fields under subfields, converts boolean fields to integers, and saves the processed data to a JSON file. Below is a detailed explanation of the script:

### Functions:

#### 1. **`fetch_data_from_api()`**
   - **Description:** Makes a GET request to the specified API endpoint (`http://localhost:8000/get_all_data`) and retrieves property data.
   - **Returns:** Fetched data as a list of property objects.
   - **Example Usage:**
     ```python
     data = fetch_data_from_api()
     ```

#### 2. **`convert_boolean_fields(data, fields_to_convert)`**
   - **Description:** Converts specified boolean fields in the data to integers (0 or 1).
   - **Parameters:**
     - `data`: List of property objects.
     - `fields_to_convert`: List of field names to convert from boolean to integer.
   - **Returns:** Processed data with specified fields converted to integers.
   - **Example Usage:**
     ```python
     data = convert_boolean_fields(data, ["field1", "field2"])
     ```

#### 3. **`group_fields_under_subfield(data, fields_to_group, subfield_name)`**
   - **Description:** Groups specified fields under a subfield in each property object.
   - **Parameters:**
     - `data`: List of property objects.
     - `fields_to_group`: List of field names to group under the subfield.
     - `subfield_name`: Name of the subfield to create.
   - **Returns:** Processed data with specified fields grouped under the specified subfield.
   - **Example Usage:**
     ```python
     data = group_fields_under_subfield(data, ["field1", "field2"], "subfield_name")
     ```

#### 4. **`save_to_json(data, filename="output.json")`**
   - **Description:** Saves the processed data to a JSON file with the specified filename (default is "output.json").
   - **Parameters:**
     - `data`: Processed data to be saved.
     - `filename`: Name of the output JSON file.
   - **Example Usage:**
     ```python
     save_to_json(data, filename="processed_data.json")
     ```

### Usage Guidelines:

1. **Fetching and Processing Data:**
   - Call `fetch_data_from_api()` to retrieve property data from the specified API endpoint.
   - Optionally, use `convert_boolean_fields()` to convert boolean fields to integers.
   - Use `group_fields_under_subfield()` to group specified fields under subfields.
   - The processed data is ready for further analysis or storage.

2. **Saving Processed Data:**
   - Call `save_to_json()` to save the processed data to a JSON file.
   - Specify the desired filename as the parameter (default is "output.json").

### Example Workflow:

```python
# Fetch data from the API
fetched_data = fetch_data_from_api()

# Convert specified boolean fields to integers
processed_data = convert_boolean_fields(fetched_data, ["field1", "field2"])

# Group specified fields under subfields
processed_data = group_fields_under_subfield(processed_data, ["field3", "field4"], "subfield_name")

# Save the processed data to a JSON file
save_to_json(processed_data, filename="processed_data.json")
```

This script enables data processing and transformation, making it suitable for various applications where data manipulation is required. Adjust the fields and subfield names in the script to match your specific use case. If you encounter any issues, refer to the error messages for troubleshooting or modify the script as needed.
