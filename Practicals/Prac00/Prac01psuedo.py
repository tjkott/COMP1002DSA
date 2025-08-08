"""BEGIN
FUNCTION Main
SET filePath = "temperatures_365_days.csv"
DECLARE dates[365] // Array to store the dates
DECLARE temperatures[365] // Array to store the temperatures
CALL readTemperatureData(filePath, dates, temperatures)
CALL findExtremeDays(dates, temperatures)
PRINT "Hottest day: " + maxDay + " with temperature " + maxTemp + "°C"
PRINT "Coldest day: " + minDay + " with temperature " + minTemp + "°C"
END
FUNCTION readTemperatureData(filePath, dates, temperatures)
OPEN file at filePath for reading
SKIP header line
SET i = 0 // Index for the arrays
WHILE there are more lines in the file
READ a line
SPLIT the line by ',' to get date and temperature
SET dates[i] = date // Store date in the array
SET temperatures[i] = temperature // Store temperature in the array
INCREMENT i by 1 // Move to the next index
END WHILE
END
FUNCTION findExtremeDays(dates, temperatures)
SET maxTemp = temperatures[0] // Initialize maxTemp with the first
temperature
SET minTemp = temperatures[0] // Initialize minTemp with the first
temperature
SET maxDay = dates[0] // Initialize maxDay with the first date
SET minDay = dates[0] // Initialize minDay with the first date
FOR i = 1 to 364 // Loop through the remaining temperatures
IF temperatures[i] > maxTemp
SET maxTemp = temperatures[i]
SET maxDay = dates[i]
END IF
IF temperatures[i] < minTemp
SET minTemp = temperatures[i]
SET minDay = dates[i]
END IF
END FOR
PRINT "Hottest day: " + maxDay + " with temperature " + maxTemp + "°C"
PRINT "Coldest day: " + minDay + " with temperature " + minTemp + "°C"
END
END"""

import csv

def main():
    csv_path = '/Users/thejanakottawatta/Documents/COMP1002DSA/Prac01/temperatures.csv'
    dates = [None] * 365  # Array to store the dates
    temperatures = [None] * 365  # Array to store the temperatures
    readTemeperatureData(csv_path, dates, temperatures)
    findExtremeDays(dates, temperatures)

def readTemeperatureData(file_path, dates, temperatures):
    with open(file_path, 'r') as csvfile:
        next(csvfile)  # Skip header line
        i = 0  # Index for the arrays
        for line in csvfile:
            parts = line.strip().split(',')
            dates[i] = parts[0]  # Store date in the array
            temperatures[i] = int(parts[1])  # Store temperature in the array
            i += 1  # Move to the next index
            if i >= 365:
                break

def findExtremeDays(dates, temperatures):
        max_temp = temperatures[0]  # Initialize maxTemp with the first temperature
        max_day = dates[0]  # Initialize maxDay with the first date
        min_temp = temperatures[0]  # Initialize minTemp with the first temperature
        min_day = dates[0]  # Initialize minDay with the first date
        for i in range(1, 365):  # Loop through the remaining temperatures
            if temperatures[i] > max_temp:
                max_temp = temperatures[i]
                max_day = dates[i]
            if temperatures[i] < min_temp:
                min_temp = temperatures[i]
                min_day = dates[i]
        print(f"Hottest day: {max_day} with temperature {max_temp}°C")
        print(f"Coldest day: {min_day} with temperature {min_temp}°C")

main()