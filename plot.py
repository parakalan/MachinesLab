import matplotlib.pyplot as plt
import math


def eff_vs_slip(V_rtd, I_rtd, W_rtd, constant_losses):
    """
        Efficiency vs Slip for two different loads

        @params:
            V_rtd - Rated voltage
            I_rtd - Rated current
            W_rtd - Rated power
            Rs    - Stator resistance
    """
    loads = [0.3, 0.6]
    plots = []
    for load in loads:
        x = [0]
        y = [0]
        for s in range(1, 100):
            slip = float(s) / 100
            p_out = load * W_rtd
            p_in = float(p_out + (1 - slip) * constant_losses) / (1 - slip)
            efficiency = float(p_out) / p_in
            y.append(efficiency)
            x.append(slip)
        plots.append(plt.plot(x, y, label = load))
    #plt.legend(handles=plots)
    plt.xlabel('Slip')
    plt.ylabel('Efficiency')
    plt.title('Efficiency vs Slip')
    plt.savefig('plots/eff_vs_slip.png')
    plt.show()


def torque_vs_slip(V_rtd, N_rtd, R_01, X_01, Rs):
    """
        Developed torque versus slip

        @params:
            V_rtd - Rated voltage
            N_rtd - Rated speed
            R_01  - Equivalent resistance referred to stator
            Rs    - Stator resistance
    """
    k = 3 * 60 / (2 * 3.14 * N_rtd)
    E_2 = float(V_rtd) / 1.732
    rotor_resistance = R_01 - Rs
    rotor_resistances = [rotor_resistance,
                         rotor_resistance + 3, rotor_resistance + 6]
    for resistance in rotor_resistances:
        x = []
        y = []
        for s in range(1, 100):
            slip = float(s) / 100
            torque_dev = float(k * slip * E_2 * E_2 * resistance) / \
                (resistance * resistance + slip * slip * X_01 * X_01)
            x.append(slip)
            y.append(torque_dev)
        plt.plot(x, y)
        plt.gca().invert_xaxis()
    plt.xlabel('Slip')
    plt.ylabel('Torque')
    plt.title('Torque vs Slip')
    plt.savefig('plots/torque_vs_slip.png')
    plt.show()


def stator_current_vs_slip(V_rtd, R_01, X_01, Rw, Xm, Rs):
    """
        Stator current vs slip

        @params:
            R_01  - Equivalent resistance referred to stator
            X_01  - Equivalent reactance referred to stator
            Xm    - Shunt reactance
            Rw    - Rhunt Resistance
            Rs    - Stator resistance
            V_rtd - Rated voltage
    """

    Z_01 = complex(R_01, X_01)
    Z_m = 1 / complex(1 / Rw, 1 / Xm)
    R_2 = R_01 - Rs
    x = []
    y = []
    for s in range(1, 101):
        slip = float(s) / 100
        R_load = R_2 * (1 / slip - 1)
        Zth = Z_01 + (R_load * Z_m) / (R_load + Z_m)
        Is = V_rtd / (1.732 * Zth)
        Is = abs(Is)
        x.append(slip)
        y.append(Is)
    plt.plot(x, y)
    plt.ylabel('Stator Current Is')
    plt.xlabel('Slip')
    plt.title('Stator current vs slip')
    plt.savefig('plots/stator_current_vs_slip.png')
    plt.show()


def speed_vs_supply_voltage(V_rtd, N_rtd, R_01, R_s):
    """
        Speed vs supply voltage

        @params:
    """
    frequencies = [50, 60]
    T = 20
    P = 4
    R_2 = R_01 - R_s
    for frequency in frequencies:
        x = []
        y = []
        for V_s in range(2, int(V_rtd), 1):
            Ns = 120 * frequency / P
            X = 2 * 3.14 * T / 60
            Y = 3 * V_s * V_s / (R_2 * Ns)
            Z = 3 * V_s * V_s / R_2
            N = float(Z) / (X + Y)
            x.append(V_s)
            y.append(N)
        plt.plot(x, y)
    plt.xlabel('Supply Voltage Vs')
    plt.ylabel('Speed N')
    plt.title("Speed vs supply voltage")
    plt.savefig('plots/speed_vs_supply_voltage.png')
    plt.show()


def speed_vs_rotor_resistance(V_rtd, N_rtd):
    """
        Speed vs rotor resistance

        @params:
            R_01  - Equivalent resistance referred to stator
            X_01  - Equivalent reactance referred to stator
            Xm    - Shunt reactance
            Rw    - Rhunt Resistance
            Rs    - Stator resistance
            V_rtd - Rated voltage
    """

    torques = [15, 20]
    for T in torques:
        x = []
        y = []
        for R_2 in range(10, 200):
            X = 2 * 3.14 * T / 60
            Y = float(3 * V_rtd * V_rtd) / (R_2 * N_rtd)
            Z = float(3 * V_rtd * V_rtd) / R_2
            N = Z / (X + Y)
            x.append(R_2)
            y.append(N)
        plt.plot(x, y)
    plt.xlabel('Rotor resistance R2')
    plt.ylabel('Speed N')
    plt.title("Speed vs rotor_resistance")
    plt.savefig('plots/speed_vs_rotor_resistance.png')
    plt.show()


def plot_performance(nameplate_details, constant_losses, equivalent_resistance):
    """
        Predetermine the performance
    """
    efficiency = []
    output_power = []
    for i in range(0, 101, 10):
        x = float(i) / 100
        num = x * nameplate_details[2]
        den = num + constant_losses + 3 * x * x * \
            nameplate_details[1] * nameplate_details[1] * equivalent_resistance
        eff = round(float(num) / den, 2)
        efficiency.append(eff)
        output_power.append(num)
    plt.plot(output_power, efficiency)
    plt.xlabel('Output Power')
    plt.ylabel('Efficiency')
    plt.title("Output Power vs Efficiency")
    plt.savefig('plots/output_power_vs_effficiency.png')
    plt.show()


def get_nameplate_details(file_details):
    """
        Get nameplate details from file.
    """
    file_details = file_details[1].split(',')
    V_rtd = float(file_details[0])
    I_rtd = float(file_details[1])
    W_rtd = float(file_details[2])
    N_rtd = float(file_details[3])
    return V_rtd, I_rtd, W_rtd, N_rtd


def get_no_load_details(file_details):
    """
        Get no load details from file
    """
    file_details = file_details[3].split(',')
    V_no_load = float(file_details[0])
    I_no_load = float(file_details[1])
    W1 = float(file_details[2])
    W2 = float(file_details[3])
    return V_no_load, I_no_load, W1, W2


def get_blocked_rotor_details(file_details):
    """
        Get blocked rotor details form file.
    """
    file_details = file_details[5].split(',')
    V_blocked_rotor = float(file_details[0])
    I_blocked_rotor = float(file_details[1])
    W_blocked_rotor = float(file_details[2])
    return V_blocked_rotor, I_blocked_rotor, W_blocked_rotor


def mach_params(V, W1, W2, I, R01):
    """
        Returns the constant losses.
    """
    W = W1 + W2
    cos_theta = float(W) / (1.732 * V * I)
    sin_theta = math.sqrt(1 - cos_theta * cos_theta)
    Iw = I * cos_theta
    Im = I * sin_theta
    Rw = float(V) / Iw
    Xm = float(V) / Im
    W_core = 3 * Iw * Iw * Rw
    W_cu_constant = 3 * I * I * R01
    return W_core + W_cu_constant, Rw, Xm


def find_circuit_params(V_sc, I_sc, W_sc):
    """
        Returns the equivalent circuit parameters.
    """
    z_01 = float(V_sc) / I_sc
    r_01 = float(W_sc) / (I_sc * I_sc)
    cos_theta_sc = float(W_sc) / (1.732 * V_sc * I_sc)
    x_01 = math.sqrt(z_01 * z_01 - r_01 * r_01)
    return z_01, r_01, x_01


if __name__ == '__main__':
    f = open('readings')
    file_details = f.readlines()
    f.close()

    nameplate_details = get_nameplate_details(file_details)
    no_load_details = get_no_load_details(file_details)
    blocked_rotor_details = get_blocked_rotor_details(file_details)

    V = float(no_load_details[0])
    I_no_load = float(no_load_details[1])
    W1 = float(no_load_details[2])
    W2 = float(no_load_details[3])

    V_sc = float(blocked_rotor_details[0])
    I_sc = float(blocked_rotor_details[1])
    W_sc = float(blocked_rotor_details[2])

    R_s = float(file_details[7])

    circuit_params = find_circuit_params(V_sc, I_sc, W_sc)
    machine_params = mach_params(V, W1, W2, I_no_load, circuit_params[1])
    constant_losses = machine_params[0]

    plot_performance(
        nameplate_details, constant_losses, circuit_params[1])
    eff_vs_slip(nameplate_details[0], nameplate_details[
                1], nameplate_details[2], constant_losses)
    torque_vs_slip(nameplate_details[0], nameplate_details[
                   3], circuit_params[1], circuit_params[2], R_s)
    stator_current_vs_slip(
        nameplate_details[0],
        circuit_params[1],
        circuit_params[2],
        machine_params[1],
        machine_params[2],
        R_s
    )
    speed_vs_supply_voltage(nameplate_details[0], nameplate_details[
                            3], circuit_params[1], R_s)
    speed_vs_rotor_resistance(nameplate_details[0], nameplate_details[3])
