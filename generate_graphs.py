import pygal
import csv
import math

def Average(lst): 
    return (sum(lst) / len(lst)) / 100

################## --- Data extraction --- ##################

N = 4700000 # Population of the Republic of Ireland

tests_vs_time = [] # Load tests_vs_time data into 2d array. [1] is first row.
i = 0
j = 0
with open('Irish COVID-19 tests vs time.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if(i > 0): # The rows exluded pertain to dates we aren't interested in.
            new_row = []
            for val in row:
                # print("["+str(i)+"]["+str(j)+"]"+val)
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
        if(i > 16 and i < 154): # The rows exluded pertain to dates we aren't interested in.
            new_row = []
            for val in row:
                # print("["+str(i)+"]["+str(j)+"]"+val)
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

for row in tests_vs_time:
    ns.append(float(row[2]))
    ps.append(float(row[4]))
for row in infections_vs_time:
    hs.append(float(row[9]))

betas = []
alphas = []
xs = []
logxs = []
for i in range(len(ns)):
    alpha = (ps[i] - hs[i]) / ns[i]
    beta = hs[i]/N
    betas.append(beta)
    alphas.append(alpha)
    x = alpha*N + beta*N
    xs.append(x)
    logxs.append(math.log(x))

'''
growthParams = []
#a = (log(x_k) - log (x_0)) / k
for i in range(1,len(ns)):
    growthParams.append((math.log(xs[i]) - math.log(xs[0])) / i)
    print("growthParams["+str(i)+"] "+str(growthParams[i-1]))
'''
'''
The variance in (c) should be a lot smaller.
Because it is the variance of an estimate of a variable,
whereas in (b) it's the variance of the underlying variable itself.
(c) is just a measure of the uncertainty of the mean,
whereas (b) is a measure of the uncertainty of a variable,
which includes both uncertainty about its mean
and how much it varies around that mean.
'''

psCumilitive = 0
hsCumilitive = 0
nsCumilitive = 0
probXis = []
probX0s = []
vrnceXs = []
vrnceXsUprBound = []
vrnceXsLwrBound = []
vrnceEmpiricalMXs = []
stdDevXs = []

interval68CLTs = []
interval95CLTs = []
interval997CLTs = []
interval68Chebys = []
interval95Chebys = []
interval997Chebys = []

for i in range(len(ns)):
    psCumilitive = psCumilitive + ps[i]
    hsCumilitive = hsCumilitive + hs[i]
    nsCumilitive = nsCumilitive + ns[i]
    probXi = ((ps[i] - hs[i]) / ns[i])
    probXis.append(probXi)
    probX0 = ((psCumilitive - hsCumilitive) / nsCumilitive)
    probX0s.append(probX0)

for i in range(len(ns)):
    ProbXiTotal = 0
    ProbXiTotal = ProbXiTotal + probXis[i]
    avrg = ProbXiTotal / (i + 1)
    diffsqrdTot = 0
    for j in range(i):
        diffsqrd = (probXis[j] - avrg) * (probXis[j] - avrg)
        diffsqrdTot = diffsqrdTot + diffsqrd
    if ((i - 1) < 1):
        vrnceX = 0
    else:
        vrnceX = diffsqrdTot / (i - 1)
    stdDevX = math.sqrt(vrnceX)
    stdDevXs.append(stdDevX)
    interval68CLTs.append(stdDevX*2)
    interval95CLTs.append(stdDevX*4)
    interval997CLTs.append(stdDevX*6)
    vrnceXUprBound = (probXis[i] + (vrnceX / 2))
    vrnceXLwrBound = (probXis[i] - (vrnceX / 2))
    vrnceX = vrnceX * 100
    vrnceXsUprBound.append(vrnceXUprBound)
    vrnceXsLwrBound.append(vrnceXLwrBound)

for i in range(len(ns) - 1):
    empiricalMX = sum(probXis[0:i+1]) / (i + 1)
    vrnceEmpiricalMX = (probXis[i] - empiricalMX)*(probXis[i] - empiricalMX)
    vrnceEmpiricalMXs.append(vrnceEmpiricalMX)
    '''
    interval68Chebys.append(math.sqrt(variances[i]) / math.sqrt(1 - 0.32) * i)
    interval95Chebys.append(math.sqrt(variances[i]) / math.sqrt(1 - 0.05) * i)
    interval997Chebys.append(math.sqrt(variances[i]) / math.sqrt(1 - 0.003) * i)
    '''
    
#################################### --- Graph generation --- ####################################

graph_one = pygal.Line(x_label_rotation=5, show_minor_x_labels=False, x_title='Days since March 18th 2020', y_title='Percent')
graph_one.title = "Probability a tested person won't have serious symptoms and tests positive, as well as the variance of such."
graph_one.x_labels = map(str, range(0, 136))
graph_one.x_labels_major = map(str, range(0, 136)[0::10])
graph_one.add('P(Xi)', probXis)
graph_one.add('Vrnce Bound Upr', vrnceXsUprBound)
graph_one.add('Vrnce Bound Lwr', vrnceXsLwrBound)
graph_one.render_to_file('graph_one.svg')

graph_two = pygal.Line(x_label_rotation=5, show_minor_x_labels=False, x_title='Days since March 18th 2020', y_title='Percent')
graph_two.title = "Variance in the empirical mean of the probability a tested person won't have serious symptoms and tests positive."
graph_two.x_labels = map(str, range(0, 136))
graph_two.x_labels_major = map(str, range(0, 136)[0::10])
graph_two.add('Vrnce of emprcl mean', vrnceEmpiricalMXs)
graph_two.render_to_file('graph_two.svg')
'''
graph_five = pygal.Line(x_label_rotation=5, show_minor_x_labels=False, x_title='Days since March 18th 2020', y_title='some kind of y thing')
graph_five.title = "dunno yet really"
graph_five.x_labels = map(str, range(0, 136))
graph_five.x_labels_major = map(str, range(0, 136)[0::10])
graph_five.add('some kind of values really', growthParams)
graph_five.render_to_file('graph_five.svg')
'''
# x axis is days(ks). y axis log_x(k)
graph_six = pygal.Line(x_label_rotation=5, show_minor_x_labels=False, x_title='Days since March 18th 2020', y_title='Log of cases')
graph_six.title = "The logs of x over time"
graph_six.x_labels = map(str, range(0, 136))
graph_six.x_labels_major = map(str, range(0, 136)[0::10])
graph_six.add('Logs of x', logxs)
graph_six.render_to_file('graph_six.svg')

trimValsBy = 19
interval68CLTs = interval68CLTs[0::trimValsBy]
interval95CLTs = interval95CLTs[0::trimValsBy]
interval997CLTs = interval997CLTs[0::trimValsBy]
interval68Chebys = interval68Chebys[0::trimValsBy]
interval95Chebys = interval95Chebys[0::trimValsBy]
interval997Chebys = interval997Chebys[0::trimValsBy]
stdDeviations = stdDevXs[0::trimValsBy]

graph_three = pygal.Bar(x_title='0->N 3 times, where each bar represents the change after 19 additional values', y_title='Span of interval in percent', style=pygal.style.styles['default']())
graph_three.title = '68, 95, & 99.7% confidence intervals vs time for P(X0 = 1) using the CLT'
j = 0
for i in range(len(interval68CLTs)):
    j += trimValsBy
    graph_three.add('', [{'value': interval68CLTs[i], 'ci': {
        'type': 'continuous', 'sample_size': j, 'stddev': stdDeviations[i], 'confidence': .68}}])
    j += trimValsBy
graph_three.add('', [{'value': 0}])
j = 0
for i in range(len(interval95CLTs)):
    j += trimValsBy
    graph_three.add('', [{'value': interval95CLTs[i], 'ci': {
        'type': 'continuous', 'sample_size': j, 'stddev': stdDeviations[i], 'confidence': .95}}])
    j += trimValsBy
graph_three.add('', [{'value': 0}])
j = 0
for i in range(len(interval997CLTs)):
    j += trimValsBy
    graph_three.add('', [{'value': interval997CLTs[i], 'ci': {
        'type': 'continuous', 'sample_size': j, 'stddev': stdDeviations[i], 'confidence': .997}}])
    j += trimValsBy
graph_three.render_to_file('graph_three.svg')

graph_three = pygal.Bar(x_title='0->N 3 times, where each bar represents the change after 19 additional values', y_title='Span of interval in percent', style=pygal.style.styles['default']())
graph_three.title = '68, 95, & 99.7% confidence intervals vs time for P(X0 = 1) using the Chebyshevs inequality'
j = 0
for i in range(len(interval68Chebys)):
    j += trimValsBy
    graph_three.add('', [{'value': interval68Chebys[i], 'ci': {
        'type': 'continuous', 'sample_size': j, 'stddev': stdDeviations[len(stdDeviations) - 1], 'confidence': .68}}])
    j += trimValsBy
graph_three.add('', [{'value': 0}])
j = 0
for i in range(len(interval95Chebys)):
    j += trimValsBy
    graph_three.add('', [{'value': interval95Chebys[i], 'ci': {
        'type': 'continuous', 'sample_size': j, 'stddev': stdDeviations[len(stdDeviations) - 1], 'confidence': .95}}])
    j += trimValsBy
graph_three.add('', [{'value': 0}])
j = 0
for i in range(len(interval997Chebys)):
    j += trimValsBy
    graph_three.add('', [{'value': interval997Chebys[i], 'ci': {
        'type': 'continuous', 'sample_size': j, 'stddev': stdDeviations[len(stdDeviations) - 1], 'confidence': .997}}])
    j += trimValsBy
graph_three.render_to_file('graph_four.svg')

'''
line_chart = pygal.Line()
line_chart.title = 'Browser usage evolution (in %)'
line_chart.x_labels = map(str, range(2002, 2013))
line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
line_chart.render_to_file('test.svg')
'''