"""
Experiment: Predict about the best price
Generate result and plot both H_Oblivious and H_Aware algorithms
"""

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def load_data_set(file_name, starting_day, period):
    # load data with specific starting date and length
    file = pd.read_csv(file_name, header=None, sep="\t", usecols=[4], skiprows=starting_day, nrows=period)
    raw_data = []
    for i in file.values.tolist():
        raw_data.append(i[0])
    return raw_data


def get_maxmin(file_name, starting_day, period):
    # get the maximum and minimum price of the specific data sample
    file = pd.read_csv(file_name, header=None, sep="\t", usecols=[4], skiprows=starting_day, nrows=period)
    raw_data = []
    for i in file.values.tolist():
        raw_data.append(i[0])
    return max(raw_data), min(raw_data)


def get_size_data(file_name):
    # return the size of the dataset
    file = pd.read_csv(file_name, header=None, sep="\t", usecols=[4])
    raw_data = []
    for i in file.values.tolist():
        raw_data.append(i[0])
    return len(raw_data)


def generate_uniform_data(file_name, period, number_of_data):
    # generate starting date uniformly in a specific range
    data_size = get_size_data(file_name)
    uniform = np.linspace(0, data_size - period, number_of_data, dtype=int)
    return uniform


def online(data, M, m):
    # pure online algorithm
    # return the payoff of the pure online algorithm
    reservation_price = sqrt(M * m)
    trade_price = first_greater_element(data, reservation_price)
    return trade_price


def first_greater_element(searching_list, element):
    # return the first element in a list which is greater than a value
    result = None
    for item in searching_list:
        if item >= (element - 0.0001):
            result = item
            break
    if result is None:
        result = searching_list[-1]
    return result


def h_aware_negative(data, v_star, Hn, Hp, eta, M, m):
    # the H_Aware algorithm with negative value of error
    # v_star: the best price
    # Hn: the upperbound of negative error
    # Hp: the upperbound of positive error
    # eta: the actual error
    # M: the upper-bound of the price
    # m: the lower-bound of the price
    # v: predicted price
    # v_prime: the reservation price
    # return the payoff
    v = v_star / (1 + eta)
    v_prime = sqrt(M * m)
    if (1 + Hn) / (1 - Hp) <= sqrt(M / m):
        v_prime = v * (1 - Hp)
    trading_price = first_greater_element(data, v_prime)
    return trading_price


def h_aware_positive(data, v_star, Hn, Hp, eta, M, m):
    # the H_Aware algorithm with negative value of error
    # v_star: the best price
    # Hn: the upperbound of negative error
    # Hp: the upperbound of positive error
    # eta: the actual error
    # M: the upper-bound of the price
    # m: the lower-bound of the price
    # v: predicted price
    # v_prime: the reservation price
    # return the payoff
    v = v_star / (1 - eta)
    v_prime = sqrt(M * m)
    if (1 + Hn) / (1 - Hp) <= sqrt(M / m):
        v_prime = v * (1 - Hp)
    trading_price = first_greater_element(data, v_prime)
    return trading_price


def h_oblivious_negative(data, v_star, eta, r):
    # the H_Oblivious algorithm with negative value of error
    # v: predicted price
    # v_prime: the reservation price
    # return the payoff
    v = v_star / (1 + eta)
    v_prime = r * v
    trading_price = first_greater_element(data, v_prime)
    return trading_price


def h_oblivious_positive(data, v_star, eta, r):
    # the H_Oblivious algorithm with positive value of error
    # v: predicted price
    # v_prime: the reservation price
    # return the payoff
    v = v_star / (1 - eta)
    v_prime = r * v
    trading_price = first_greater_element(data, v_prime)
    return trading_price


def plot_h_aware(result_list, eta_list_all, H_list, average_pure_online, average_best_price, save_path, x_label,
                 y_label, title):
    # plot the result of H_Aware algorithm
    fig, ax = plt.subplots()
    for i in range(len(result_list)):
        ax.plot(eta_list_all[i], result_list[i], label='$H_n$=%0.2f, $H_p$=%0.2f' % (H_list[i][0], H_list[i][1]))
    ax.axhline(average_pure_online, color='black', ls='dotted', label='Pure Online')
    ax.axhline(average_best_price, color='red', ls='dotted', label='Best Price')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.legend()
    fig.savefig(save_path)
    plt.show()


def plot_h_oblivious(result, eta_list, r_list, pure_online, best_price, save_path, x_label, y_label, title):
    # plot the result of H_Oblivious algorithm
    fig, ax = plt.subplots()
    for i in range(len(result)):
        ax.plot(eta_list, result[i], label='r=%0.2f' % (r_list[i]))
    ax.axhline(pure_online, color='black', ls='dotted', label='Pure Online')
    ax.axhline(best_price, color='red', ls='dotted', label='Best Price')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.legend()
    fig.savefig(save_path)
    plt.show()


def save_to_csv_ho(payoff_list, eta_list, r_list, csv_path, pure_online, best_price):
    # save the result of H_oblivious algorithm into csv file
    myDict = {"eta": eta_list, "pure online": [pure_online] * len(eta_list),
              "best price": [best_price] * len(eta_list)}
    for i in range(len(r_list)):
        myDict["payoff(r=%0.2f)" % r_list[i]] = payoff_list[i]
    df = pd.DataFrame.from_dict(myDict, orient='index').transpose()
    df.to_csv(csv_path)


def save_to_csv_ha(payoff_list, eta_list, H_list, csv_path, pure_online, best_price):
    # save the result of H_Aware algorithm into csv file
    myDict = {}
    for i in range(len(H_list)):
        myDict["eta(Hn=%0.2f, Hp=%0.2f)" % (H_list[i][0], H_list[i][1])] = eta_list[i]
        myDict["payoff(Hn=%0.2f, Hp=%0.2f)" % (H_list[i][0], H_list[i][1])] = payoff_list[i]
    myDict["pure online"] = [pure_online] * len(eta_list[-1])
    myDict["best price"] = [best_price] * len(eta_list[-1])
    df = pd.DataFrame.from_dict(myDict, orient='index').transpose()
    df.to_csv(csv_path)


def main():
    # choose dataset
    #data_name = "ETHUSD"
    #data_name = "BTCUSD"
    #data_name = "CADJPY"
    data_name = "EURUSD"

    fileName = "data/" + data_name + ".csv"  # choose the dataset

    whole_period = 250  # set the whole period to 250 days
    trading_period = 200  # set the trading period to 200 days
    eta_coefficient = 100  # the coefficient determines how many data point for error
    quantity_of_data = 20  # the number of data sample

    # H_Oblivious Algorithm
    uniform_list = generate_uniform_data(fileName, 250, quantity_of_data)
    average_pure_online = 0
    average_best_price = 0

    r_list = [0.5, 0.75, 1, 1.5]  # the value of r to experiment
    result_list = list()  # create the list of payoff for different value of r for H_Oblivious algorithm
    Hn_max = 0
    Hp_max = 0

    # generate a universal eta list for all Hn and Hp value
    for starting_day in uniform_list:
        M, m = get_maxmin(fileName, starting_day, whole_period)
        Hn_bound_float = (M - m) / m  # the upper-bound of the value of negative error
        Hp_bound_float = (M - m) / M  # the upper-bound of the value of positive error
        # convert Hn and Hp to 2 decimal
        Hn_bound = round(Hn_bound_float, 2)
        Hp_bound = round(Hp_bound_float, 2)

        if Hn_bound > Hn_bound_float:
            Hn_bound = Hn_bound - 0.01

        if Hp_bound > Hp_bound_float:
            Hp_bound = Hp_bound - 0.01

        if Hn_bound > Hn_max:
            Hn_max = Hn_bound

        if Hp_bound > Hp_max:
            Hp_max = Hp_bound

    whole_eta = np.arange(-Hn_max, Hp_max + 0.01, 0.01).tolist()
    whole_eta = [round(x, 2) for x in whole_eta]

    for starting_day in uniform_list:
        data = load_data_set(fileName, starting_day, trading_period)
        M, m = get_maxmin(fileName, starting_day, whole_period)
        pure_online = online(data, M, m)
        v_star = max(data)

        Hn_bound_float = (M - m) / m  # the upper-bound of the value of negative error
        Hp_bound_float = (M - m) / M  # the upper-bound of the value of positive error

        # convert Hn and Hp to 2 decimal
        Hn_bound = round(Hn_bound_float, 2)
        Hp_bound = round(Hp_bound_float, 2)

        if Hn_bound > Hn_bound_float:
            Hn_bound = Hn_bound - 0.01

        if Hp_bound > Hp_bound_float:
            Hp_bound = Hp_bound - 0.01

        average_pure_online += pure_online  # sum the payoff of pure online for all data sample
        average_best_price += v_star  # sum the best price for all data sample

        sample_result = list()

        for r in r_list:
            # create the list of negative and positive value of eta
            eta_list_n = np.arange(0, Hn_bound + 0.01, 0.01).tolist()
            del (eta_list_n[0])

            eta_list_p = np.arange(0, Hp_bound + 0.01, 0.01).tolist()
            # create the list of negative and positive value of payoff
            payoff_list_n = list()
            payoff_list_p = list()

            # calculate payoff for each value of eta
            for eta_n in eta_list_n:
                payoff_list_n.append(h_oblivious_negative(data, v_star, eta_n, r))
            for eta_p in eta_list_p:
                payoff_list_p.append(h_oblivious_positive(data, v_star, eta_p, r))

            payoff_list = payoff_list_n[::-1] + payoff_list_p

            eta_list_n = [-x for x in eta_list_n]
            eta_list = eta_list_n[::-1] + eta_list_p
            eta_list = [round(x, 2) for x in eta_list]

            left_index = whole_eta.index(eta_list[0])
            right_index = whole_eta.index(eta_list[-1])

            payoff_list = [0] * left_index + payoff_list + [0] * (len(whole_eta) - right_index - 1)

            sample_result.append(payoff_list)

        result_list.append(sample_result)

    payoff_h1 = list()
    payoff_h2 = list()
    payoff_h3 = list()
    payoff_h4 = list()
    for sample_list in result_list:
        payoff_h1.append(np.array(sample_list[0]))
        payoff_h2.append(np.array(sample_list[1]))
        payoff_h3.append(np.array(sample_list[2]))
        payoff_h4.append(np.array(sample_list[3]))

    array_h1 = np.array(payoff_h1, dtype=object)
    array_h2 = np.array(payoff_h2, dtype=object)
    array_h3 = np.array(payoff_h3, dtype=object)
    array_h4 = np.array(payoff_h4, dtype=object)

    count_zero_h1 = array_h1.T
    count_zero_h2 = array_h2.T
    count_zero_h3 = array_h3.T
    count_zero_h4 = array_h4.T

    average_number_h1 = list()
    average_number_h2 = list()
    average_number_h3 = list()
    average_number_h4 = list()

    for i in count_zero_h1:
        average_number_h1.append(np.count_nonzero(i))
    result_h1 = list(array_h1.sum(axis=0))

    for i in range(len(result_h1)):
        result_h1[i] = result_h1[i] / average_number_h1[i]

    for i in count_zero_h2:
        average_number_h2.append(np.count_nonzero(i))
    result_h2 = list(array_h2.sum(axis=0))

    for i in range(len(result_h2)):
        result_h2[i] = result_h2[i] / average_number_h2[i]

    for i in count_zero_h3:
        average_number_h3.append(np.count_nonzero(i))
    result_h3 = list(array_h3.sum(axis=0))

    for i in range(len(result_h1)):
        result_h3[i] = result_h3[i] / average_number_h3[i]

    for i in count_zero_h4:
        average_number_h4.append(np.count_nonzero(i))
    result_h4 = list(array_h4.sum(axis=0))

    for i in range(len(result_h4)):
        result_h4[i] = result_h4[i] / average_number_h4[i]

    result = [result_h1, result_h2, result_h3, result_h4]
    average_pure_online = average_pure_online / quantity_of_data  # calculate the average payoff of pure online for all data samples
    average_best_price = average_best_price / quantity_of_data  # calculte the average best price for all data samples

    save_path_ho = "experiment_result/" + data_name + "/" + data_name + "_h_oblivious.png"  # the path to save the figure

    # plot the h_oblivious figure
    plot_h_oblivious(result, whole_eta, r_list, average_pure_online, average_best_price, save_path=save_path_ho,
                     x_label="error $\eta$", y_label="Payoff", title="H-Oblivious")
    # the path to save the csv file
    csv_path_ho = "experiment_result/" + data_name + "/" + "H_oblivious.csv"
    # save the result of h_oblivious algorithm to csv file
    save_to_csv_ho(result, whole_eta, r_list, csv_path_ho, average_pure_online, average_best_price)

    # H_Aware Algorithm
    # generate starting date uniformly from the dataset
    uniform_list = generate_uniform_data(fileName, 250, quantity_of_data)
    result_list = list()
    average_pure_online = 0
    average_best_price = 0
    # generate different combo of Hn and Hp
    Hn_Hp_list = [(0.05, 0.05), (0.1, 0.1), (0.2, 0.2), (0.2, 0.3), (0.3, 0.3), (0.4, 0.4), (0.5, 0.5)]

    # take the average payoff from all data sample
    for starting_day in uniform_list:
        data = load_data_set(fileName, starting_day, trading_period)
        M, m = get_maxmin(fileName, starting_day, whole_period)
        pure_online = online(data, M, m)
        v_star = max(data)

        average_pure_online += pure_online  # sum the payoff of pure online for all data sample
        average_best_price += v_star  # sum the best price for all data sample

        sample_result = list()
        eta_list_all = list()

        # for different value of Hn and Hp, calculate eta list and payoff list
        for hn_hp in Hn_Hp_list:
            eta_list_n = np.linspace(0, hn_hp[0], int(hn_hp[0] * eta_coefficient + 1)).tolist()
            eta_list_p = np.linspace(0, hn_hp[1], int(hn_hp[1] * eta_coefficient + 1)).tolist()
            payoff_list_n = list()
            payoff_list_p = list()

            for eta_n in eta_list_n:
                payoff_list_n.append(h_aware_negative(data, v_star, hn_hp[0], hn_hp[1], eta_n, M, m))

            for eta_p in eta_list_p:
                payoff_list_p.append(h_aware_positive(data, v_star, hn_hp[0], hn_hp[1], eta_p, M, m))

            payoff_list = payoff_list_n[::-1] + payoff_list_p

            eta_list_n = [-x for x in eta_list_n]
            eta_list = eta_list_n[::-1] + eta_list_p

            payoff_array = np.array(payoff_list)
            eta_list_all.append(eta_list)

            sample_result.append(payoff_array)
            sample_array = np.array(sample_result, dtype=object)

        result_list.append(sample_array)
        result_array = np.array(result_list)

    result = list(result_array.mean(axis=0))
    average_pure_online = average_pure_online / quantity_of_data  # calculate the average payoff of pure online for all data samples
    average_best_price = average_best_price / quantity_of_data  # calculte the average best price for all data samples

    save_path_ha = "experiment_result/" + data_name + "/" + data_name + "_h_aware.png"

    # plot H_aware
    plot_h_aware(result, eta_list_all, Hn_Hp_list, average_pure_online, average_best_price, save_path_ha,
                 "error $\eta$", "Average Payoff", "H-Aware")
    # the path to save the result of h-aware

    csv_path_ha = "experiment_result/" + data_name + "/" + "H_aware.csv"

    # save the result to csv file
    save_to_csv_ha(result, eta_list_all, Hn_Hp_list, csv_path_ha, average_pure_online, average_best_price)


if __name__ == '__main__':
    main()
