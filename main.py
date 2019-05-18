# Sources
# Presidential candidate receipts and  disbursements
    # https://www.fec.gov/data/candidates/president/?election_year=2020&cycle=2020&election_full=true
# Presidntial candidate popular and electoral votes
    # https://www.britannica.com/topic/United-States-Presidential-Election-Results-1788863

import json 
import math
import statistics 
import matplotlib.pyplot as plt
import numpy as np

REGRESSION_TYPE = "QUADRATIC"


def least_squares_quadratic(x_list, y_list):
    assert len(x_list) == len(y_list)
    n = len(x_list)

    summation_x = sum(x_list) 

    summation_x_squared = 0
    for x in x_list:
        summation_x_squared += x**2

    summation_x_cubed = 0
    for x in x_list:
        summation_x_cubed += x**3

    summation_x_fourth = 0
    for x in x_list:
        summation_x_fourth += x**4

    summation_y = sum(y_list)

    summation_x_y = 0
    for x, y in zip(x_list, y_list):
        summation_x_y += x * y 

    summation_x_squared_y = 0
    for x, y in zip(x_list, y_list):
        summation_x_squared_y += (x**2) * y 

    a = np.array([
        [summation_x_squared, summation_x, n],
        [summation_x_cubed, summation_x_squared, summation_x],
        [summation_x_fourth, summation_x_cubed, summation_x_squared],
    ])

    b = np.array([
        [summation_y],
        [summation_x_y],
        [summation_x_squared_y]
    ])

    constants = np.linalg.solve(a, b)

    return (constants[0][0], constants[1][0], constants[2][0])

def least_squares_linear(x_list, y_list):
    def compute_a(x_list, y_list, b):
        x_bar = statistics.mean(x_list)
        y_bar = statistics.mean(y_list)

        return y_bar - (b * x_bar)

    def compute_b(x_list, y_list):
        assert len(x_list) == len(y_list)

        n = len(x_list)

        summation_x_y = 0
        for x, y in zip(x_list, y_list):
            summation_x_y += x * y 

        summation_x_squared = 0
        for i in x_list:
            summation_x_squared += x**2

        numerator = summation_x_y - (sum(x_list) * sum(y_list) / n)
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
    constants = ()

    for d in json_data:
        x_data = d[kwargs["x"]]
        y_data = d[kwargs["y"]]
        
        if d.get("party") == "Democrat":
            democrat_x.append(x_data)
            democrat_y.append(y_data)
        if d.get("party") == "Republican":
            republican_x.append(x_data)
            republican_y.append(y_data)

    # republican_data = (array of republican x, array of republican y)
    # democrat_data = (array of democrat x, array of democrat y)

    republican_data = (republican_x, republican_y)
    democrat_data = (democrat_x, democrat_y)
    all_x = republican_x + democrat_x
    all_y = republican_y + democrat_y

    if _type == "LINEAR":
        constants = least_squares_linear(all_x, all_y)
    
    if _type == "EXPONENTIAL":
        constants = least_squares_exponential(all_x, all_y)
    
    if _type == "QUADRATIC":
        constants = least_squares_quadratic(all_x, all_y)
    
    return (republican_data, democrat_data, constants)

def create_plot(plot_data, title, categories, _type):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
    colors = ("red", "blue", "green")
    groups = ("Republican", "Democrat", "Least Squares Line")
    regression_line_equation = ""
    
    for i, (ipd, color, group) in enumerate(zip(plot_data, colors, groups)):
        print(i)
        print("ipd: ", ipd)
        # Plots X and Y points in the scatter plot
        if i != 2:
            x, y = ipd
            ax.scatter(x, y, alpha=0.8, c=color, edgecolors="none", s=30, label=group)

        # Plots the linear regression line
        if i == 2:
            print("in 2")
            # Get X values for linear regression and save into x_plot
            all_x = plot_data[0][0] + plot_data[1][0]
            x_range = max(all_x) - min(all_x)
            x_increments = x_range / len(all_x)
            x_plot = list(range(0, int(max(all_x)), int(x_increments)))
            
            # Get Y values for linear regression
            y_plot = []
            
            if _type == "LINEAR":
                a, b = ipd
                y_plot = [a + (b * _x) for _x in x_plot]
                regression_line_equation = "y = {}x + {}".format(b, a)
            elif _type == "EXPONENTIAL":
                a, b = ipd
                y_plot = [math.e**(a + b * _x) for _x in x_plot]
                regression_line_equation = "y = e^({} + {}x)".format(a, b)
            elif _type == "QUADRATIC":
                a, b, c = ipd 
                y_plot = [a*(_x**2) +  b*_x + c for _x in x_plot]
                regression_line_equation = "y = {}x^2 + {}x + {} ".format(a, b, c)

            plt.plot(x_plot, y_plot, "m-")

    plt.ylabel(categories["y"])
    plt.xlabel("{}\n{}".format(categories["x"], regression_line_equation))
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

    plot_data = get_data(json_data, REGRESSION_TYPE, **categories)

    print("Republican {}: ".format(categories["x"]), plot_data[0][0])
    print("Republican {}: ".format(categories["y"]), plot_data[0][1])

    print("Democrat {}: ".format(categories["x"]), plot_data[1][0])
    print("Democrat {}: ".format(categories["y"]), plot_data[1][1])

    create_plot(plot_data, "Candidate {} vs. {}".format(categories["x"], categories["y"]), categories, REGRESSION_TYPE)
