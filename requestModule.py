import requests
import json
class RequestModule:
    def __init__(self, host: str, token: str, stock_cd: str):
        self.host = host
        self.token = token
        self.stock_cd = stock_cd

    def get_cur_price(self) -> float:
        # TODO: 임시로 네이버증권에서 크롤링해옴
        res = requests.get('https://polling.finance.naver.com/api/realtime/domestic/stock/005930')
        data = json.loads(res.text)
        data = data['datas'][0]['closePrice'].replace(',', '')
        return float(data)
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
    
    def get_history_price(self) -> list[int]:
        # 삼성증권 종가 가져오기
        url = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey=7gKP2xmAVmttq49TdewQul7EWG00fR4Iv3hActo3gj2bBhCE22c5dMXcIx%2FRsMmkms63ue6Gn%2B3rg4nxLFpauA%3D%3D&numOfRows=500&resultType=json&itmsNm=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90'
        res = requests.get(url)
        data = json.loads(res.text)
        data = list(map(lambda x: int(x['clpr']), data['response']['body']['items']['item']))
        return data
    
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