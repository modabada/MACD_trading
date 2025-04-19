from requestModule import RequestModule

if __name__ == "__main__":
    rm = RequestModule("https://api.example.com", "your_token", "your_stock_cd")
    rm.get_cur_price()