from typing import List, Optional

from kmeans.utils import list_euclidean_dist, list_calc_mean

class GraphPoint:
    def __init__(self, location: List[float], gp_id: int, name: Optional[str] = None, ):
        self.location = location
        self.nearest_value_id = -1
        self.nearest_value_dist = float("inf")
        self.name = name
        self.gp_id = gp_id


class CentroidPoint:
    def __init__(self, location: List[float], centroid_id: int):
        self.location = location
        self.centroid_id = centroid_id


#------------------------------------------------------------------------------
        
def check_closer_centroid(centroid_point: CentroidPoint, graph_point: GraphPoint)-> None:
    dist = list_euclidean_dist(pointA=centroid_point.location, pointB=graph_point.location)
    if dist < graph_point.nearest_value_dist:
        graph_point.nearest_value_id = centroid_point.centroid_id
        graph_point.nearest_value_dist = dist


def reset_graph_point(graph_point: GraphPoint)->None:
    graph_point.nearest_value_id = -1
    graph_point.nearest_value_dist = float("inf")


#------------------------------------------------------------------------------
    
def refocus_centroid(centroid_point: CentroidPoint, graph_points: List[GraphPoint])->bool:
    id_graph_points = [
        graph_point.location
        for graph_point in graph_points
        if graph_point.nearest_value_id == centroid_point.centroid_id
    ]

    new_location = list_calc_mean(lists = id_graph_points)

    # if not new_location:
    #     raise ValueError(f"centroid isolated at: {centroid_point.location}\nPlease redefine centroid locations or remove from pool")
    
    if new_location == centroid_point.location:
        return False
    
    centroid_point.location = new_location
    return True

#------------------------------------------------------------------------------

def kmeans(centroid_points: List[CentroidPoint], graph_points: List[GraphPoint])->None:
    for _ in range(100):
        for centroid_point in centroid_points:
            for graph_point in graph_points:
                check_closer_centroid(centroid_point=centroid_point, graph_point=graph_point)

            centroid_updated = False
            for centroid_point in centroid_points:
                did_update = refocus_centroid(
                    centroid_point=centroid_point, graph_points=graph_points
                )
                if did_update:
                    centroid_updated = True

        if not centroid_updated:
            return
        
        for graph_point in graph_points:
            reset_graph_point(graph_point=graph_point)