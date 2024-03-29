# //=============================================================================
# //Radosław Tecmer)
# //(c)Copyright (2023) free of copyright
# //-----------------------------------------------------------------------------
# //The program communicates with the PLC Siemens S7 1200 (300).
# //Generates a variable using the math.sin() function.
# // Amplitude range adjustable with min and max parameters, frequency and phase.
# //-----------------------------------------------------------------------------
# //contact:
# //https://github.com/remceTkedaR
# //radek69tecmer@gmail.com
# //=============================================================================


import time
import snap7.exceptions
import struct
import math


class WaterPressureSimulator:
    def __init__(self):
        self.amplitude = 3.45  # Amplituda sygnału sinusoidalnego
        self.frequency = 0.1  # Częstotliwość sygnału sinusoidalnego
        self.phase = 0.0      # Faza sygnału sinusoidalnego (początkowa)
        self.bar_out = 0.0

    def simulate(self):
        # Generowanie sygnału sinusoidalnego w zakresie od 0.1 do 7.0
        self.bar_out = 3.45 + 3.45 * math.sin(2 * math.pi * self.frequency + self.phase)

        # Przesunięcie fazy
        self.phase += 0.01

        # Ograniczenie wartości do zakresu od 0.1 do 7.0
        if self.bar_out < 0.1:
            self.bar_out = 0.1
        elif self.bar_out > 7.0:
            self.bar_out = 7.0


# konfiguracja połaczenie ze sterownikiem PLC S7 300
plc_ip = '192.168.3.203'
plc = snap7.client.Client()
plc.connect(plc_ip, 0, 2)

if __name__ == "__main__":
    # Inicjalizacja symulatora ciśnienia wody
    simulator = WaterPressureSimulator()

    try:
        while True:
            # Symulacja ciśnienia wody na podstawie sygnału sinusoidalnego
            simulator.simulate()

            print(f"Process Variable: {simulator.bar_out}")

            # Przekazanie wartości do bloku danych sterownika PLC
            data_bytes = struct.pack("!f", simulator.bar_out)
            plc.db_write(1, 0, data_bytes)

            time.sleep(1)  # Czekaj przez sekundę przed kolejnym pomiar

    except KeyboardInterrupt:
        # Zatrzymanie programu po wciśnięciu Ctrl+C
        pass

    # Wynik działania symulacji
    final_pressure = simulator.bar_out
    print(f"Final Pressure: {final_pressure}")
