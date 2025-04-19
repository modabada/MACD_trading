import requests

class RequestModule:
    def __init__(self, host: str, token: str, stock_cd: str):
        self.host = host
        self.token = token
        self.stock_cd = stock_cd

    def get_cur_price(self) -> int:
        # TODO: Implement the logic to get the current price from the URL
        return 1000

    def buy_order(self, amount: int) -> bool:
        # TODO: Implement the logic to make an order
        
        returnMsg = "정상적으로 처리되었습니다"
        if returnMsg == "정상적으로 처리되었습니다":
            return True
        return False

    def sell_order(self, amount: int) -> bool:
        # TODO : Implement the logic to make an order
        returnMsg = "매도주문이 완료되었습니다"
        if returnMsg == "매도주문이 완료되었습니다":
            return True
        return False
    
    def _request(self, endpoint: str, apiId: str):
        url = f"{self.host}/{endpoint}"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		    'authorization': f'Bearer {self.token}', # 접근토큰
		    # 'cont-yn': cont_yn, # 연속조회여부
		    # 'next-key': next_key, # 연속조회키
		    'api-id': apiId, # TR명
	    }
        response = requests.post(url, headers=headers)
        return response.json()