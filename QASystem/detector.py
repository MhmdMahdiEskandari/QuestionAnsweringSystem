import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_average_step(array, threshold=5):
    """
    Determine the average step by doing a weighted average based on clustering of averages.
    array: our array
    threshold: the +/- offset for grouping clusters. Aplicable on all elements in the array.
    """

    # determine all the steps
    steps = []
    for i in range(0, len(array) - 1):
        steps.append(abs(array[i] - array[i+1]))

    # determine the steps clusters
    clusters = []
    skip_indexes = []
    cluster_index = 0

    for i in range(len(steps)):
        if i in skip_indexes:
            continue

        # determine the cluster band (based on threshold)
        cluster_lower = steps[i] - (steps[i]/100) * threshold
        cluster_upper = steps[i] + (steps[i]/100) * threshold

        # create the new cluster
        clusters.append([])
        clusters[cluster_index].append(steps[i])

        # try to match elements from the rest of the array
        for j in range(i + 1, len(steps)):

            if not (cluster_lower <= steps[j] <= cluster_upper):
                continue

            clusters[cluster_index].append(steps[j])
            skip_indexes.append(j)

        cluster_index += 1  # increment the cluster id

    clusters = sorted(clusters, key=lambda x: len(x), reverse=True)
    biggest_cluster = clusters[0] if len(clusters) > 0 else None

    if biggest_cluster is None:
        return None

    return sum(biggest_cluster) / len(biggest_cluster)  # return our most common average


def detect_anomalous_values(array, regular_step, threshold=20):
    """
    Will scan every triad (3 points) in the array to detect anomalies.
    array: the array to iterate over.
    regular_step: the step around which we form the upper/lower band for filtering
    treshold: +/- variation between the steps of the first and median element and median and third element.
    """
    assert(len(array) >= 3)  # must have at least 3 elements

    anomalous_indexes = []

    # step_lower = regular_step - (regular_step / 100) * threshold
    step_lower = 0
    step_upper = regular_step + (regular_step / 100) * threshold

    # detection will be forward from i (hence 3 elements must be available for the d)
    for i in range(0, len(array) - 2):
        a = array[i]
        b = array[i+1]
        c = array[i+2]

        first_step = abs(a-b)
        second_step = abs(b-c)

        first_belonging = step_lower <= first_step <= step_upper
        second_belonging = step_lower <= second_step <= step_upper

        # detect that both steps are alright
        if first_belonging and second_belonging:
            continue  # all is good here, nothing to do

        # detect if the first point in the triad is bad
        if not first_belonging and second_belonging:
            anomalous_indexes.append(i)

        # detect the last point in the triad is bad
        if first_belonging and not second_belonging:
            anomalous_indexes.append(i+2)

        # detect the mid point in triad is bad (or everything is bad)
        if not first_belonging and not second_belonging:
            anomalous_indexes.append(i+1)
            # we won't add here the others because they will be detected by
            # the rest of the triad scans

    return sorted(set(anomalous_indexes))  # return unique indexes

# if __name__ == "__main__":
#
#     N = 10                  # Set signal sample length
#     t1 = -np.pi             # Simulation begins at t1
#     t2 =  np.pi;            # Simulation  ends  at t2
#
#     in_array = np.linspace(t1, t2, N)
#
#     # add some noise
#     noise_input = random.uniform(-.5, .5);
#     in_array[random.randint(0, len(in_array)-1)] = noise_input
#     noisy_out_array = np.sin(in_array)
#
#     # display noisy sin
#     plt.figure()
#     plt.plot(in_array, noisy_out_array, color = 'red', marker = "o");
#     plt.title("noisy numpy.sin()")
#
#     # detect anomalous values
#     average_step = calculate_average_step(in_array)
#     anomalous_indexes = detect_anomalous_values(in_array, average_step)
#
#     # replace anomalous points with an estimated value based on our calculated average
#     for anomalous in anomalous_indexes:
#
#         # try forward extrapolation
#         try:
#             in_array[anomalous] = in_array[anomalous-1] + average_step
#         # else try backwward extrapolation
#         except IndexError:
#             in_array[anomalous] = in_array[anomalous+1] - average_step
#
#     # generate sine wave
#     out_array = np.sin(in_array)
#
#     plt.figure()
#     plt.plot(in_array, out_array, color = 'green', marker = "o");
#     plt.title("cleaned numpy.sin()")
#
#     plt.show()