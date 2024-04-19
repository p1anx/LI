
def token_cal(input, output):
    usd_cny = 7.2
    price1 = input*(10*usd_cny/1e6)
    price2 = output * (30*usd_cny/1e6)
    # print = price1 + price2
    print(f"price = {price1 + price2}")
    print(f"price1: {price1}, price2: {price2}\n")
def array_cat():
    a = [1, 2, 3]
    b = [4, 5, 6]
    c = a + b
    print(f"c:{c}\n")

if __name__ == "__main__":
    print("Hello, World!")
    # token_cal(6628, 662)
    array_cat()