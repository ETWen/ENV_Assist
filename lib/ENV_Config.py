import configparser
import matplotlib.pyplot as plt
import numpy as np


class PROFILE_PLOT_SETTING():
    def __init__(self):
        return
    def PROF_TEMP():
        # Read the configuration file
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Parse the data
        cmd_lst = []
        steps = []
        temperatures = []
        durations = []
        current_temp = 25  # Assume initial temperature is 25°C
        time_points = [0]
        temperature_points = [current_temp]
        pgm_num = config['Chamber CONFIG']['PGM_NUM']
        cmd_start = f"PRGM DATA WRITE, PGM{pgm_num}, EDIT START"
        #print(cmd_start)
        cmd_lst.append(cmd_start)

        for step in sorted(config['Chamber PROFILE'].keys(), key=lambda x: int(x[4:])):
            profile = config['Chamber PROFILE'][step].split(',')
            step_name = profile[0].strip()
            target_temp = float(profile[1].strip())
            duration = float(profile[2].strip())

            #print(step, step_name, target_temp, duration)
            cmd_line = f"PRGM DATA WRITE, PGM{pgm_num}, {step.upper()}, {step_name}, GRANTY ON, TRAMP OFF, TEMP{target_temp}, TIME{str(duration).replace('.', ':')}"
            #print(cmd_line)
            cmd_lst.append(cmd_line)
            
            if step_name == 'TRAMP':
                # Handle temperature gradient changes
                start_temp = current_temp
                end_temp = target_temp
                time_increment = 0.01  # Time step for gradient change in hours
                num_points = int(duration / time_increment)
                
                for i in range(1, num_points + 1):
                    intermediate_temp = start_temp + (end_temp - start_temp) * (i / num_points)
                    temperature_points.append(intermediate_temp)
                    time_points.append(time_points[-1] + time_increment)
                
                current_temp = end_temp
            else:
                # Handle constant temperature
                temperature_points.append(target_temp)
                time_points.append(time_points[-1] + duration)
                current_temp = target_temp
            
            steps.append(step_name)
            temperatures.append(target_temp)
            durations.append(duration)

        cmd_end = f"PRGM DATA WRITE, PGM{pgm_num}, EDIT END"
        #print(cmd_end)
        cmd_lst.append(cmd_end)
        '''
        for cmd_idx in cmd_lst:
            print(cmd_idx)
        '''

        # Plot the temperature profile
        plt.figure(figsize=(10, 5))
        plt.plot(time_points, temperature_points, label='Temperature Profile', drawstyle='steps-post')

        # Set X-axis ticks interval to 0.5 hours
        #plt.xticks(np.arange(0, time_points[-1] + 0.5, 0.5))
        plt.xticks(np.arange(0, time_points[-1] + 1, 1))

        # Add labels and title
        plt.xlabel('Time (hours)')
        plt.ylabel('Temperature (°C)')
        plt.title('Chamber Temperature Profile')
        plt.grid(True)
        plt.legend()

        # Save the plot as a file (e.g., PNG format)
        plt.savefig('temperature_profile.png')

        # Show the plot
        # plt.show()

        return cmd_lst

