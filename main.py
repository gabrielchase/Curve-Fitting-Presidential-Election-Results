# Sources
# Presidential candidate receipts and  disbursements
    # https://www.fec.gov/data/candidates/president/?election_year=2020&cycle=2020&election_full=true
# Presidntial candidate popular and electoral votes
    # https://www.britannica.com/topic/United-States-Presidential-Election-Results-1788863

import json 
import statistics 
import matplotlib.pyplot as plt


def compute_b(x_list, y_list):
    assert len(x_list) == len(y_list)
    
    # b = (∑XY−((∑X)(∑Y)/n)) / ∑X**2−((∑X)2n)
    
    summation_x_times_y = 0
    summation_x_squared = 0
    n = len(x_list)
    
    # Iterate through x_list and y_list
        # multiply x * y
        # add to summation_x_times_y
    for x, y in zip(x_list, y_list):
        summation_x_times_y += x * y 
    
    for i in x_list:
        summation_x_squared += x**2

    print('Numerator: ')
    print(summation_x_times_y, sum(x_list), sum(y_list), n)
    numerator = summation_x_times_y - (sum(x_list) * sum(y_list) / n)
    print('Denominator: ')
    print(summation_x_squared, (sum(x_list)**2), n)
    denomimator = summation_x_squared - ((sum(x_list)**2) / n)

    return numerator / denomimator

def compute_a(x_list, y_list, b):
    x_bar = statistics.mean(x_list)
    y_bar = statistics.mean(y_list)

    return y_bar - (b * x_bar)

def flatten_list(*args):
    flattened_list = []
    
    for arg in args:
        if isinstance(arg, list):
            for i in arg:
                flattened_list.append(i)

    return flattened_list

def method_of_least_squares(x1, x2, y1, y2):
    # ∑Y=na+b∑X
    # ∑XY=a∑X+b∑X2

    all_x = flatten_list(x1, x2)
    all_y = flatten_list(y1, y2)

    b = compute_b(all_x, all_y)
    a = compute_a(all_x, all_y, b)
   
    print('a: ', a)
    print('b: ', b)

    return (a, b)


def get_data(json_data, **kwargs):
    republican_x = []
    republican_y = []
    democrat_x = []
    democrat_y = []

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
    least_squares_line = method_of_least_squares(republican_x, democrat_x, republican_y, democrat_y)
    
    return (republican_data, democrat_data, least_squares_line)

def create_plot(plot_data, title, categories):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
    colors = ("red", "blue", "green")
    groups = ("Republican", "Democrat", "Least Squares Line")
    
    for i, (ith_plot_data, color, group) in enumerate(zip(plot_data, colors, groups)):
        x, y = ith_plot_data
        if i != 2:
            ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", s=30, label=group)
        if i == 2:
            a = x 
            b = y 

            print('plot_data: ', plot_data)
            all_x = flatten_list(plot_data[0][0], plot_data[1][0])

            x_plot = []

            x_range = max(all_x) - min(all_x)
            x_increments = x_range / len(all_x)

            x_plot = list(range(0, int(max(all_x)), int(x_increments)))
            y_plot = [a + (b * _x) for _x in x_plot]

            print('{} + ({} * x)'.format(a, b))

            plt.plot(x_plot, y_plot, 'm-')

    regression_line_equation = 'y = {}x + {}'.format(plot_data[2][1], plot_data[2][0])

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
        "x": "disbursements", 
        "y": "popular_votes"
    }

    plot_data = get_data(json_data, **categories)

    
    print('Republican {}: '.format(categories['x']), plot_data[0][0])
    print('Republican {}: '.format(categories['y']), plot_data[0][1])

    print('Democrat {}: '.format(categories['x']), plot_data[1][0])
    print('Democrat {}: '.format(categories['y']), plot_data[1][1])

    create_plot(plot_data, "Candidate {} vs. {}".format(categories["x"], categories["y"]), categories)
