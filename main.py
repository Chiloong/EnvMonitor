from wind import check_wind
from pressure import check_pressure
from fusion import check_fusion

def main():
    check_wind()
    check_pressure()
    check_fusion()  # 联动模块仅处理逻辑，不重复调用 check_pressure()

if __name__ == "__main__":
    main()
