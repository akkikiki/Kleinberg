# coding: utf-8
import numpy as np
import scipy as sp
import math
from scipy.misc import comb 
import sys

def detect_burst(relevant_list, total_list):
    """ Assume (num. of relevant docs, total num. docs) as the two input lists
        returns state costs
    """
    
    state_costs = [(0.0, 0.0)] # for the initial step
    s = 2
    R = sum(relevant_list)
    D = sum(total_list)
    p_0 = (1.0 * R) / D    
    p_1 = p_0 * s
    n = len(relevant_list)
    for i in range(n):
        r_t = relevant_list[i]
        d_t = total_list[i]
        nonburst_state_cost = calc_state_cost(0, r_t, d_t, p_0)
        burst_state_cost = calc_state_cost(1, r_t, d_t, p_1)
        state_costs.append((nonburst_state_cost, burst_state_cost))

    print state_costs
    best_state_sequence = calc_best_state_sequence(state_costs)

    return best_state_sequence

def calc_state_cost(i, r_t, d_t, p_i):
    coef = comb(d_t, r_t, exact=True) # binomial coefficient
    #print coef, p_i
    return -1.0 * (math.log(coef) + r_t * math.log(p_i) + (d_t - r_t) * math.log(1 - p_i))

#def calculate_weight():
#    """ Calculating the weight of the bursts. Used for ranking the detected bursts
#    """

def calc_transition_cost(current_state, next_state, r):
    cost = 0
    if next_state > current_state:
        cost = r * (next_state - current_state)
    return cost

def calc_best_state_sequence(state_costs, r = 1):
    """ State costs: (non-burst state cost, burst state cost)
    """
    n = len(state_costs)
    subtotal_cost = 0 # unnecessary?
    current_state = 0 # non-burst state
    best_state_sequence = []

    for j in range(n):
        #current_state_cost = state_costs[j][current_state]
        to_burst_state = state_costs[j][1] + calc_transition_cost(current_state, 1, r)
        to_nonburst_state = state_costs[j][0] + calc_transition_cost(current_state, 0, r)
        #import ipdb; ipdb.set_trace()

        best_cost = 0
        if to_burst_state < to_nonburst_state: 
            best_cost = to_burst_state 
            current_state = 1
        else:
            best_cost = to_nonburst_state
            current_state = 0
        
        best_state_sequence.append(current_state)
        subtotal_cost += best_cost

    return best_state_sequence

def main():
    f = open(sys.argv[1])
    f_out = open(sys.argv[1] + "_predicted_burst_timestamps", "w")
    relevant_list = []
    total_list = []

    for line in f:
        relevant, total = map(int, line[:-1].split("\t"))
        relevant_list.append(relevant)
        total_list.append(total)

    best_state_sequence = detect_burst(relevant_list, total_list)
    print best_state_sequence

    for i in range(1, len(best_state_sequence)):
      f_out.write(str(best_state_sequence[i]) + "\n")

if __name__ == "__main__":
    main()
