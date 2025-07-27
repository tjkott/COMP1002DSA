import csv

csv_path = '/Users/thejanakottawatta/Documents/COMP1002DSA/Prac01/temperatures.csv'
temperatures = []

with open(csv_path, 'r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        temp_str = row.get('Temperature (°C)', '').strip()
        if temp_str:
            try:
                temp = int(temp_str)
                temperatures.append(temp)
            except ValueError:
                pass

if temperatures:
    max_temp = max(temperatures)
    min_temp = min(temperatures)
    print(f"Output: Max Temperature: {max_temp}°C, Min Temperature: {min_temp}°C")
else:
    print("No valid temperature data found.")
