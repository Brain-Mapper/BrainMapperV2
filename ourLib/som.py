import tkinter

import numpy as np
from neupy import algorithms, utils
from scipy.spatial import distance

utils.reproducible()

grid_height = 20
grid_width = 20
HEIGHT = 800 / grid_height
WIDTH = 800 / grid_width

data_raw = np.array([[-63.0, 7.0, 30.0, 1],
                     [-63.5, 7.5, 24.0, 1],
                     [-64.0, 6.0, 24.0, 0],
                     [-65.0, 8.0, 16.0, 1],
                     [-61.0, 16.0, 18.0, 0],
                     [0, 0, 0, 1],
                     ])

data = [e[:3] for e in data_raw]
last_column = [e[3:] for e in data_raw]

sofm = algorithms.SOFM(
    # Use only two features for the input
    n_inputs=3,

    # In clustering application we will prefer that
    # clusters will be updated independently from each
    # other. For this reason we set up learning radius
    # equal to zero
    learning_radius=2,

    # Parameters controls learning rate for each neighbour. The further neighbour neuron from the 		#winning neuron the smaller that learning rate for it. Learning rate scales based on the 		#factors produced by the normal distribution with center in the place of a winning neuron and 		#standard deviation specified as a parameter. The learning rate for the winning neuron is 		#always equal to the value specified in the step parameter and for neighbour neurons it’s 		#always lower.
    std=1,  # TODO : modifier

    # Feature grid defines shape of the output neurons. The new shape should be compatible with 		#the number of outputs
    features_grid=(grid_height, grid_width),

    # Defines connection type in feature grid
    grid_type='rect',

    # Defines function that will be used to compute closest weight to the input sample
    distance='euclid',

    # Instead of generating random weights
    # (features / cluster centers) SOFM will sample
    # them from the data. Which means that after
    # initialization step 3 random data samples will
    # become cluster centers
    # weight='sample_from_data',

    # Training step size or learning rate
    step=0.25,

    # Shuffles dataset before every training epoch.
    shuffle_data=True,

    # Shows training progress in terminal
    verbose=True,
)
sofm.train(data, epochs=10)
sofm.predict(data)

weight = sofm.weight
param_length = sofm.weight.shape[0]
param_width = sofm.weight.shape[1]

neurons = []
for j in range(param_width):
    temp = []
    for i in range(param_length):
        temp.append(weight[i, j])
    neurons.append(temp)

data_neuron_index = []

for k in data:
    the_closest_neuron = 0
    distance_min = distance.euclidean(k, neurons[0])
    indice = 0
    for l in range(len(neurons)):
        new_distance = distance.euclidean(k, neurons[l])
        if new_distance < distance_min:
            distance_min = new_distance
            indice = l
    data_neuron_index.append(indice)

fenetre = tkinter.Tk()

fenetre.title("SOM")
Terrain = tkinter.Canvas(fenetre, height=800, width=800)
Terrain.pack()
carreau = []
for j in range(grid_width):
    temp = []
    for i in range(grid_height):
        color = "#cdcdcd"
        value = j * grid_height + i + 1

        if value in data_neuron_index:
            index = data_neuron_index.index(value)
            param = last_column[index][0]
            if param == 1:
                color = "#ff5f00"
            else:
                color = "#000000"
        # Cas où pas de neurones
        temp.append(Terrain.create_rectangle(i * HEIGHT, j * WIDTH, (i + 1) * HEIGHT, (j + 1) * WIDTH, fill=color))

    carreau.append(temp)

# Coord=tkinter.Label(fenetre)
# Coord.pack(pady='10px')

fenetre.mainloop()
