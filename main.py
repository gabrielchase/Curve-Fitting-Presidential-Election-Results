# Sources
# Presidential candidate receipts and  disbursements
    # https://www.fec.gov/data/candidates/president/?election_year=2020&cycle=2020&election_full=true
# Presidntial candidate popular and electoral votes
    # https://www.britannica.com/topic/United-States-Presidential-Election-Results-1788863

import json 
import math
import statistics 
import matplotlib.pyplot as plt


def least_squares_linear(x_list, y_list):
    def compute_a(x_list, y_list, b):
        x_bar = statistics.mean(x_list)
        y_bar = statistics.mean(y_list)

        return y_bar - (b * x_bar)

    def compute_b(x_list, y_list):
        assert len(x_list) == len(y_list)

        summation_x_times_y = 0
        summation_x_squared = 0
        n = len(x_list)

        for x, y in zip(x_list, y_list):
            summation_x_times_y += x * y 

        for i in x_list:
            summation_x_squared += x**2

        numerator = summation_x_times_y - (sum(x_list) * sum(y_list) / n)
        denomimator = summation_x_squared - ((sum(x_list)**2) / n)

        return numerator / denomimator

    b = compute_b(x_list, y_list)
    a = compute_a(x_list, y_list, b)

    return (a, b)

def least_squares_exponential(x_list, y_list):
    def compute_a(x_list, y_list, b):
        assert len(x_list) == len(y_list)
        n = len(x_list)
        
        summation_ln_y = 0
        for y in y_list:
            summation_ln_y += math.log(y)
        
        summation_x = sum(x_list)

        return ((1 / n) * (summation_ln_y)) - ((b / n) * summation_x)

    def compute_b(x_list, y_list):
        assert len(x_list) == len(y_list)
        n = len(x_list)

        summation_x_ln_y = 0
        for x, y in zip(x_list, y_list):
            summation_x_ln_y += x * math.log(y)

        summation_x = sum(x_list)

        summation_ln_y = 0
        for y in y_list:
            summation_ln_y += math.log(y)

        summation_x_squared = 0
        for x in x_list:
            summation_x_squared += x**2

        numerator = (n * summation_x_ln_y) - (summation_x * summation_ln_y)
        denominator = (n * summation_x_squared) - summation_x**2

        return numerator/denominator

    b = compute_b(x_list, y_list)
    a = compute_a(x_list, y_list, b)

    return (a, b)


def get_data(json_data, _type, **kwargs):
    republican_x = []
    republican_y = []
    democrat_x = []
    democrat_y = []
    least_squares_line = ()

    for d in json_data:
        x_data = d[kwargs["x"]]
        y_data = d[kwargs["y"]]
        
        if d.get('party') == "Democrat":
            democrat_x.append(x_data)
            democrat_y.append(y_data)
        if d.get('party') == "Republican":
            republican_x.append(x_data)
            republican_y.append(y_data)

    # republican_data = (array of republican x, array of republican y)
    # democrat_data = (array of democrat x, array of democrat y)

    republican_data = (republican_x, republican_y)
    democrat_data = (democrat_x, democrat_y)
    all_x = republican_x + democrat_x
    all_y = republican_y + democrat_y

    if _type == 'LINEAR':
        least_squares_line = least_squares_linear(all_x, all_y)
    
    if _type == 'EXPONENTIAL':
        least_squares_line = least_squares_exponential(all_x, all_y)
    
    return (republican_data, democrat_data, least_squares_line)

def create_plot(plot_data, title, categories, _type):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
    colors = ("red", "blue", "green")
    groups = ("Republican", "Democrat", "Least Squares Line")
    regression_line_equation = ''
    
    for i, (ith_plot_data, color, group) in enumerate(zip(plot_data, colors, groups)):
        x, y = ith_plot_data
        if i != 2:
            ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", s=30, label=group)
        if i == 2:
            a = x 
            b = y 

            all_x = plot_data[0][0] + plot_data[1][0]

            x_plot = []

            x_range = max(all_x) - min(all_x)
            x_increments = x_range / len(all_x)

            x_plot = list(range(0, int(max(all_x)), int(x_increments)))
            y_plot = []
            
            if _type == 'LINEAR':
                y_plot = [a + (b * _x) for _x in x_plot]
                regression_line_equation = 'y = {}x + {}'.format(b, a)
            if _type == 'EXPONENTIAL':
                y_plot = [math.e**(a + b * _x) for _x in x_plot]
                regression_line_equation = 'y = e^({} + {}x)'.format(a, b)

            plt.plot(x_plot, y_plot, 'm-')


    plt.ylabel(categories["y"])
    plt.xlabel('{}\n{}'.format(categories["x"], regression_line_equation))
    plt.title(title)
    plt.legend(loc=2)
    plt.show()


def load_json_data(file_name):
    with open(file_name) as f:
        return json.load(f)

if __name__ == "__main__":
    json_data = load_json_data("data.json")

    categories = {
        "x": "receipts", 
        "y": "popular_vote"
    }

    plot_data = get_data(json_data, 'EXPONENTIAL', **categories)

    
    print('Republican {}: '.format(categories['x']), plot_data[0][0])
    print('Republican {}: '.format(categories['y']), plot_data[0][1])

    print('Democrat {}: '.format(categories['x']), plot_data[1][0])
    print('Democrat {}: '.format(categories['y']), plot_data[1][1])

    create_plot(plot_data, "Candidate {} vs. {}".format(categories["x"], categories["y"]), categories, 'EXPONENTIAL')
