from wind import check_wind
from pressure import check_pressure
from fusion import check_fusion

def main():
    wind_data = check_wind()
    pressure_data = check_pressure()
    check_fusion(wind_data, pressure_data)

if __name__ == "__main__":
    main()
