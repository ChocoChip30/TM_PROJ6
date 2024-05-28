import csv
import copy
import math
from typing import List
import os

#------------------------------------------------------------------------------
def read_csv(filePath: str)->List[str]:
    data = []
    with open(filePath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(list(row.values()))
    return data

def convert_str_list_to_float_list(myList: List[str])->List[float]:
    return [float(item) for item in myList]


#------------------------------------------------------------------------------
def list_euclidean_dist(pointA: List[float], pointB: List[float])->float:
    vector_delta_squared = [
        (a - b)**2 for a, b in zip(pointA, pointB)
    ]
    return math.sqrt(sum(vector_delta_squared))

def list_calc_mean(lists: List[List[float]])->List[float]:
    # takes a list of lists as input and outputs a list
    # containing the means of each of the inner lists
    mean_list = []
    list_length = len(lists)
    for values in zip(*lists):
        mean = sum(values)/list_length
        mean_list.append(mean)

    return mean_list

#------------------------------------------------------------------------------
if __name__ == "__main__":

    data = read_csv("/Users/tamaramarie/Desktop/CODE/ProteinBarRecommender/ProteinBarRecommender/assets/new_data.csv")
    html_auto = open("template.html", "w")
    my_code = ""
    for index, bar in enumerate(data):
        my_code += f'''
        <!-- {bar[1]} -->
        <div class = "row" >
            <div class = "col-sm-1"></div>
            <div class = "col-sm-10">
                <input class="form-check-input" type="checkbox" value="{bar[1].lower()}" id="{bar[0]}" onclick="console.log({bar[0]})">
                <label class="form-check-label" for="{bar[1].lower().replace(' ','-')}">{bar[1].capitalize()}</label>
            </div>
            <div class = "col-sm-1"></div>
        </div>
        '''
    html_auto.write(my_code)
    html_auto.close()
