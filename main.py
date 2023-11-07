from fastapi import FastAPI, Query
import time
import psutil

import httpx
import json

app = FastAPI()

# Create a global async client to reduce overhead
client = httpx.AsyncClient()

# Use an async generator to fetch data in chunks
async def fetch_data_in_chunks(cursor=0):
    while True:
        # url = f"https://login.streetwise24.com/api/1.1/obj/property?agency=1694504430615x780232707323405000&constraints=[{{\"key\":\"Online\",\"constraint_type\":\"equals\",\"value\":\"1\"}}]&cursor={cursor}"
        url = f"https://login.streetwise24.com/api/1.1/obj/property?agency=1694504430615x780232707323405000&cursor={cursor}"
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

        results = data["response"]["results"]
        remaining = data["response"]["remaining"]

        yield results
        cursor += 100

        if remaining == 0:
            break

# Fetch and sort data in a single async function
async def fetch_and_sort_data(sort_param):
    results = []
    async for chunk in fetch_data_in_chunks():
        results.extend(chunk)

    return sort_data(results, sort_param)

# Sort data
def sort_data(data, sort_param):
    if sort_param == "price_asc":
        data.sort(key=lambda x: float(x.get("Price", 0)))
    elif sort_param == "price_desc":
        data.sort(key=lambda x: float(x.get("Price", 0)), reverse=True)
    elif sort_param == "date_new":
        data.sort(key=lambda x: x.get("Created Date", ""), reverse=True)
    elif sort_param == "date_old":
        data.sort(key=lambda x: x.get("Created Date", ""))
    return data

@app.get("/get_all_data")
async def get_all_data():
    start_time = time.time()
    cpu_usage = psutil.cpu_percent()

    all_data = await fetch_and_sort_data(None)

    end_time = time.time()
    cpu_usage_after = psutil.cpu_percent()

    cpu_usage_diff = cpu_usage_after - cpu_usage
    execution_time = end_time - start_time
    
    print("----------------------------------------")
    print("get_all_data function execution time:")
    print(execution_time, "seconds")
    print("CPU usage:")
    print(cpu_usage_diff, "%")
    print("----------------------------------------")

    return {"data": all_data}

@app.get("/data")
async def get_data_file(
    city: str = Query(None, title="City", description="Filter data by city"),
    min_price: float = Query(None, title="Minimum Price", description="Filter data by minimum price"),
    max_price: float = Query(None, title="Maximum Price", description="Filter data by maximum price"),
    bedrooms: int = Query(None, title="Number of Bedrooms", description="Filter data by number of bedrooms"),
    sort: str = Query(None, title="Sort", description="Sort data by 'price_asc', 'price_desc', 'date_new', or 'date_old'"),
    return_city_only: bool = Query(False, title="Return City Only", description="Return only the city of every object")
):
    try:
        # Load data from JSON file (simulated data)
        with open("output.json", "r") as json_file:
            data = json.load(json_file)

        # Filter data
        filtered_data = []
        for item in data:
            item_price = float(item.get("Price", 0))
            item_bedrooms = int(item.get("Bedrooms", 0))
            if (city is None or item.get("City") == city) and \
               (min_price is None or item_price >= min_price) and \
               (max_price is None or item_price <= max_price) and \
               (bedrooms is None or item_bedrooms > bedrooms):
                if return_city_only:
                    filtered_data.append(item.get("City"))
                else:
                    filtered_data.append(item)

        # Sort data
        if sort:
            filtered_data = sort_data(filtered_data, sort)

        return filtered_data
    except FileNotFoundError:
        return {"error": "Output file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON file"}
    except Exception as e:
        return {"error": str(e)}
