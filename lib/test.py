import matplotlib.pyplot as plt
import re

# Sample data (replace with your actual data)
data = [
    "1,TEMP25.0,TEMP RAMP OFF,HUMI50,HUMI RAMP OFF,TIME0:00,GRANTY OFF,REF9,PAUSE OFF",
    "2,TEMP25.0,TEMP RAMP OFF,HUMI50,HUMI RAMP OFF,TIME4:00,GRANTY OFF,REF9,PAUSE OFF",
    "3,TEMP50.0,TEMP RAMP ON,HUMI5,HUMI RAMP ON,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "4,TEMP50.0,TEMP RAMP OFF,HUMI5,HUMI RAMP OFF,TIME24:00,GRANTY OFF,REF9,PAUSE OFF",
    "5,TEMP50.0,TEMP RAMP OFF,HUMI95,HUMI RAMP ON,TIME4:00,GRANTY OFF,REF9,PAUSE OFF",
    "6,TEMP50.0,TEMP RAMP OFF,HUMI95,HUMI RAMP OFF,TIME17:00,GRANTY OFF,REF9,PAUSE OFF",
    "7,TEMP50.0,TEMP RAMP OFF,HUMI50,HUMI RAMP ON,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "8,TEMP65.0,TEMP RAMP ON,HUMI50,HUMI RAMP OFF,TIME4:00,GRANTY OFF,REF9,PAUSE OFF",
    "9,TEMP65.0,TEMP RAMP OFF,HUMI90,HUMI RAMP ON,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "10,TEMP65.0,TEMP RAMP OFF,HUMI90,HUMI RAMP OFF,TIME24:00,GRANTY OFF,REF9,PAUSE OFF",
    "11,TEMP65.0,TEMP RAMP OFF,HUMI50,HUMI RAMP ON,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "12,TEMP50.0,TEMP RAMP ON,HUMI50,HUMI RAMP OFF,TIME4:00,GRANTY OFF,REF9,PAUSE OFF",
    "13,TEMP50.0,TEMP RAMP OFF,HUMI95,HUMI RAMP ON,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "14,TEMP50.0,TEMP RAMP OFF,HUMI95,HUMI RAMP OFF,TIME11:00,GRANTY OFF,REF9,PAUSE OFF",
    "15,TEMP50.0,TEMP RAMP OFF,HUMI50,HUMI RAMP ON,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "16,TEMP50.0,TEMP RAMP OFF,HUMI50,HUMI RAMP OFF,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "17,TEMP25.0,TEMP RAMP ON,HUMI50,HUMI RAMP OFF,TIME2:00,GRANTY OFF,REF9,PAUSE OFF",
    "18,TEMP25.0,TEMP RAMP ON,HUMI50,HUMI RAMP OFF,TIME24:00,GRANTY OFF,REF9,PAUSE OFF"
]

data2 = [
    "1,TEMP50.0,TEMP RAMP OFF,HUMI5,HUMI RAMP OFF,TIME24:00,GRANTY OFF,REF9,PAUSE OFF"
]

data3 = [
    "1,TEMP25.0,TEMP RAMP OFF,HUMI OFF,TIME4:10,GRANTY OFF,REF9,PAUSE OFF",
    "2,TEMP-5.0,TEMP RAMP ON,HUMI OFF,TIME1:00,GRANTY OFF,REF9,PAUSE OFF",
    "3,TEMP-5.0,TEMP RAMP OFF,HUMI OFF,TIME4:00,GRANTY OFF,REF9,PAUSE OFF",
    "4,TEMP-40.0,TEMP RAMP ON,HUMI OFF,TIME1:30,GRANTY OFF,REF9,PAUSE OFF",
    "5,TEMP-40.0,TEMP RAMP OFF,HUMI OFF,TIME4:00,GRANTY OFF,REF9,PAUSE OFF",
    "6,TEMP-5.0,TEMP RAMP ON,HUMI OFF,TIME1:30,GRANTY OFF,REF9,PAUSE OFF"
]

# Function to parse the data
def parse_data(data):
    temp_values = []
    humi_values = []
    cumulative_time = []
    total_minutes = 0

    for line in data:
        parts = line.split(',')
        if len(parts) >= 5:
            temp = float(parts[1].replace("TEMP", ""))
            humi = parts[3].replace("HUMI", "").strip()
            if humi == "OFF":
                humi = None
            else:
                humi = float(humi)
            
            time_part = re.search(r'TIME(\d+:\d+)', line).group(1)
            hours, minutes = map(int, time_part.split(':'))
            total_minutes += hours * 60 + minutes
            total_hours = total_minutes / 60
            
            temp_values.append(temp)
            humi_values.append(humi)
            cumulative_time.append(total_hours)
    
    return temp_values, humi_values, cumulative_time

# Function to plot temperature and humidity on two subplots with dual X-axes
def plot_temp_humi_subplots(data):
    temp_values, humi_values, cumulative_time = parse_data(data)
    
    # Add origin point with the same values as the first data point
    temp_values.insert(0, temp_values[0])
    humi_values.insert(0, humi_values[0])
    cumulative_time.insert(0, 0)
    steps = range(0, len(temp_values))

    # Create a figure with two subplots (2 rows, 1 column)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Create twin axes for steps
    twin_ax1 = ax1.twiny()
    twin_ax2 = ax2.twiny()
    
    # Plotting temperature on the first subplot
    ax1.plot(cumulative_time, temp_values, marker='o', linestyle='-', color='b', label='Temperature')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_xlim(0)  # Set Y axis limits for temperature
    ax1.set_ylim(-50, 75)  # Set Y axis limits for temperature
    ax1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    ax1.xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax1.legend()
    
    twin_ax1.set_xlim(ax1.get_xlim())
    twin_ax1.set_xticks(cumulative_time)
    twin_ax1.set_xticklabels(steps)
    twin_ax1.set_xlabel('Steps')

    # Plotting humidity on the second subplot
    humi_cumulative_time = [time for time, humi in zip(cumulative_time, humi_values) if humi is not None]
    humi_values_filtered = [humi for humi in humi_values if humi is not None]
    ax2.plot(humi_cumulative_time, humi_values_filtered, marker='o', linestyle='-', color='g', label='Humidity')
    ax2.set_xlabel('Cumulative Time (hr)')
    ax2.set_ylabel('Humidity (%)')
    ax2.set_xlim(0)  # Set Y axis limits for temperature
    ax2.set_ylim(0, 100)  # Set Y axis limits for humidity
    ax2.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    ax2.xaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax2.legend()
    
    twin_ax2.set_xlim(ax2.get_xlim())
    twin_ax2.set_xticks(cumulative_time)
    twin_ax2.set_xticklabels(steps)
    twin_ax2.set_xlabel('Steps')

    # Set the window title after calling plot function
    plt.gcf().canvas.manager.set_window_title('Custom Window Title')

    # Adjust layout and show the plot
    fig.tight_layout()
    plt.show()

# Example usage
plot_temp_humi_subplots(data2)
