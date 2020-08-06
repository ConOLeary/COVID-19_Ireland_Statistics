import pygal
import csv

# --- Data extraction --- #

N = 4904000 # Population of the Republic of Ireland

tests_vs_time = [] # Load tests_vs_time data into 2d array. [1] is first row.
i = 0
j = 0
with open('Irish COVID-19 tests vs time.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        new_row = []
        for val in row:
            print("["+str(i)+"]["+str(j)+"]"+val)
            new_row.append(val)
            j+=1
        tests_vs_time.append(new_row)
        j = 0
        i+=1

infections_vs_time = [] # Load infections_vs_time data into 2d array. [1] is first row.
i = 0
j = 0
with open('Irish COVID-19 infections vs time.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        new_row = []
        for val in row:
            print("["+str(i)+"]["+str(j)+"]"+val)
            new_row.append(val)
            j+=1
        infections_vs_time.append(new_row)
        j = 0
        i+=1


# Each element of the following arrays pertains to a day,
#  starting from 2020/03/18 00:00:00.
ns = [] # This is the total number n of tests carried out for COVID-19.
ps = [] # The number p of tests which were positive.
hs = [] # The number h of infected people hospitalised.


# --- Graph generation --- #
graph_one_a = pygal.Line()
graph_one_a.title = "Probability that i'th person without serious symptims tests positive"



"""
line_chart = pygal.Line()
line_chart.title = 'Browser usage evolution (in %)'
line_chart.x_labels = map(str, range(2002, 2013))
line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
line_chart.render_to_file('test.svg')
"""