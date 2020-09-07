import pygal
import csv
import math

#################################### --- Data extraction --- ####################################

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


#################################### --- Data processing --- ####################################

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

probXis = []
meanProbXis = []
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

    probXi = ((ps[i] - hs[i]) / ns[i])
    probXis.append(probXi)

for i in range(len(ns)):
    ProbXiTotal = 0
    ProbXiTotal = ProbXiTotal + probXis[i]
    avrgXi = ProbXiTotal / (i + 1)
    meanProbXis.append(avrgXi)
    diffsqrdTot = 0
    for j in range(i):
        diffsqrd = (probXis[j] - avrgXi)**2
        diffsqrdTot = diffsqrdTot + diffsqrd
    if ((i - 1) < 1):
        vrnceX = 0
    else:
        vrnceX = diffsqrdTot / (i - 1)
    vrnceXUprBound = (probXis[i] + (vrnceX / 2))
    vrnceXLwrBound = (probXis[i] - (vrnceX / 2))
    vrnceX = vrnceX * 100 # For cosmetic reasons on graph
    vrnceXsUprBound.append(vrnceXUprBound)
    vrnceXsLwrBound.append(vrnceXLwrBound)
    stdDevX = math.sqrt(vrnceX)
    stdDevXs.append(stdDevX)

    interval95Chebys.append((math.sqrt(vrnceX / 0.05)))
    # sqrt(variance / 0.05) = 2 * x  

for i in range(len(ns) - 1):
    metaMean = sum(meanProbXis[0:i+1]) / (i + 1)
    diffsqrdTot = 0
    for j in range(i):
        diffsqrd = (meanProbXis[j] - metaMean)**2
        diffsqrdTot = diffsqrdTot + diffsqrd
    if ((i - 1) < 1):
        metaVrnceX = 0
    else:
        metaVrnceX = diffsqrdTot / (i - 1)
    vrnceEmpiricalMXs.append(metaVrnceX)


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
graph_two.title = "Variance of the empirical mean of the probability a tested person won't have serious symptoms and tests positive."
graph_two.x_labels = map(str, range(0, 136))
graph_two.x_labels_major = map(str, range(0, 136)[0::10])
graph_two.add('Vrnce of emprcl mean', vrnceEmpiricalMXs)
graph_two.render_to_file('graph_two.svg')

trimValsBy = 10
trmdProbXis = probXis[0::trimValsBy]
trmdInterval95Chebys = interval95Chebys[0::trimValsBy]

graph_three = pygal.Bar(x_title="Days", y_title='Percent', style=pygal.style.styles['default']())
graph_three.title = ''
j = 0
for i in range(len(trmdProbXis)):
    graph_three.add('', [{'value': trmdProbXis[i], 'ci': {
        'type': 'continuous', 'sample_size': ns[i*trimValsBy], 'stddev': stdDevXs[i*trimValsBy], 'confidence': .95}}])
graph_three.title = "Confidence intervals of estimates of Prob(X0 = 1) using the Central Limit Theorem"
graph_three.render_to_file('graph_three.svg')

graph_four = pygal.Bar(x_title="Days", y_title='Percent', style=pygal.style.styles['default']())
graph_four.title = ''
j = 0
for i in range(len(trmdInterval95Chebys)):
    graph_four.add('', [{'value': trmdProbXis[i], 'ci': {'low': trmdProbXis[i]-(trmdInterval95Chebys[i]/200), 'high': trmdProbXis[i]+(trmdInterval95Chebys[i]/200)}}])
graph_four.title = "Confidence intervals of estimates of Prob(X0 = 1) using Chebyshev's Inequality"
graph_four.render_to_file('graph_four.svg')

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