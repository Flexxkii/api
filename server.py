import requests
import json

def fetch_data_from_api():
    try:
        response = requests.get("http://localhost:8000/get_all_data")
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return data["data"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def convert_boolean_fields(data, fields_to_convert):
    for item in data:
        for field in fields_to_convert:
            if field in item:
                item[field] = int(item[field])
    return data

def group_fields_under_subfield(data, fields_to_group, subfield_name):
    for item in data:
        subfield_data = {}
        for field in fields_to_group:
            if field in item:
                subfield_data[field] = item.pop(field)
        item[subfield_name] = subfield_data
    return data

def save_to_json(data, filename="output.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data has been saved to {filename}")

if __name__ == "__main__":
    fields_to_group = ["room_living_room_facilitites", "room_kitchen_facilitites", "room_toilet_facilitites", "room_bathroom_facilitites", "room_bedroom_facilitites"]  # Add other fields to group
    fields_to_group2 = ["Huisdieren", "Muziek-instrument", "Energy_label", "Elevator", "Flooring", "Garden", "Heatings", "Maintenance_indoor", "Maintenance_outdoor", "Price_on_request", "Rental_period", "Roofterrace", "Smoking Allowed", "Balcony", "Servicekosten yes/no", "Kadestraal_owner"]  # Add other fields to group
    subfield_name = "facilities"  # Specify the subfield name
    subfield_name2 = "info"  # Specify the subfield name

    fetched_data = fetch_data_from_api()

    if fetched_data:
        grouped_data = group_fields_under_subfield(fetched_data, fields_to_group, subfield_name)
        grouped_data2 = group_fields_under_subfield(grouped_data, fields_to_group2, subfield_name2)
        save_to_json(grouped_data2, filename="output.json")
    else:
        print("Failed to fetch data from the API.")
