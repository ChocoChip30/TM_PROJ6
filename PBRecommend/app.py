from flask import Flask, render_template, request, jsonify
from typing import List
from copy import deepcopy

from kmeans.kmeans import GraphPoint, CentroidPoint, kmeans
from kmeans.utils import read_csv, convert_str_list_to_float_list, list_euclidean_dist, list_calc_mean

CSV_DATA = read_csv(filePath="/Users/tamaramarie/Desktop/CODE/ProteinBarRecommender/ProteinBarRecommender/assets/new_data.csv")
BAR_DATA = [
    GraphPoint(location=convert_str_list_to_float_list(data[2:]),gp_id=data[0], name=data[1])
    for data in CSV_DATA
]

# for gp in BAR_DATA:
#     print(gp.gp_id, gp.name)

CENTROIDS = [
    CentroidPoint(location=BAR_DATA[37].location, centroid_id=BAR_DATA[37].gp_id),
    CentroidPoint(location=BAR_DATA[51].location, centroid_id=BAR_DATA[51].gp_id),
    CentroidPoint(location=BAR_DATA[75].location, centroid_id=BAR_DATA[75].gp_id),
]

kmeans(centroid_points=CENTROIDS, graph_points=BAR_DATA)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    bar_data_copy = deepcopy(BAR_DATA)
    selected_bars = request.json['selectedBars']
    # Process the selected bars as needed
    selected_bar_gp = []
    selected_bar_names = []
    for s in selected_bars:
        i = int(s)
        selected_bar_gp.append(
            GraphPoint(location=BAR_DATA[i-1].location, gp_id=BAR_DATA[i-1].gp_id, name=BAR_DATA[i-1].name)
        )
        selected_bar_names.append(BAR_DATA[i-1].name)


    selected_mean = list_calc_mean(
        lists=[bar.location for bar in selected_bar_gp]
    )

    for bar in bar_data_copy:
        bar.nearest_value_dist = list_euclidean_dist(
            pointA=selected_mean, pointB=bar.location
        )

    bar_data_copy.sort(key=lambda bar: bar.nearest_value_dist)

    recommendations = []
    i = 0
    index = 0
    while i < 5:
        if bar_data_copy[index].name not in selected_bar_names:
            recommendations.append(bar_data_copy[index].name)
            i += 1
        index += 1

            
    # for index in range(5):
    #     recommendations.append(bar_data_copy[index].name)

    # Dummy response, replace with your actual recommendation logic
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)
