# Sources
# Presidential candidate receipts and  disbursements
    # https://www.fec.gov/data/candidates/president/?election_year=2020&cycle=2020&election_full=true
# Presidntial candidate popular and electoral votes
    # https://www.britannica.com/topic/United-States-Presidential-Election-Results-1788863

import json 
import matplotlib.pyplot as plt

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
    return (republican_data, democrat_data)

def create_plot(plot_data, title):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
    colors = ("red", "blue")
    groups = ("Republican", "Democrat")
    
    for plot_data, color, group in zip(plot_data, colors, groups):
        republican_data, democrat_data = plot_data
        ax.scatter(republican_data, democrat_data, alpha=0.8, c=color, edgecolors="none", s=30, label=group)

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
        "y": "popular_votes"
    }

    plot_data = get_data(json_data, **categories)
    
    print('Republican {}: '.format(categories['x']), plot_data[0][0])
    print('Republican {}: '.format(categories['y']), plot_data[0][1])

    print('Democrat {}: '.format(categories['x']), plot_data[1][0])
    print('Democrat {}: '.format(categories['y']), plot_data[1][1])

    create_plot(plot_data, "Candidate Receipts vs. Popular Votes")
