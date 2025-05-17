import requests
import json


class RequestModule:
    def __init__(self, host: str, appkey: str, secretkey: str, stock_cd: str):
        self.host = host
        self.appkey = appkey
        self.secretkey = secretkey
        self.stock_cd = stock_cd
        self.token = _get_bearer(host=host, appkey=appkey, secretkey=secretkey,)

    def __del__(self):
        self._revoke_bearer()
        print('Request module deleted')

    def get_cur_price(self) -> float:
        res = self._post(
            endpoint='/api/dostk/stkinfo',
            body={'stk_cd': self.stock_cd}
        )

        if res['return_code'] != 0:
            raise Exception(f'현재가 가져오기 실패: {response['return_msg']}')
        
        # 왜인지는 모르겠으나, 앞에 - 기호가 붙는 경우 확인,
        return abs(float(res['cur_prc']))

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
    
    def _post(self, endpoint: str, body: dict) -> json:
        url = f"{self.host}/{endpoint}"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		    'authorization': f'Bearer {self.token}', # 접근토큰
		    # 'cont-yn': cont_yn, # 연속조회여부
		    # 'next-key': next_key, # 연속조회키
		    'api-id': 'ka10001', # TR명
	    }
        response = requests.post(url, headers=headers, json=body)
        return response.json()
    
    def _revoke_bearer(self):
        url = f"{self.host}/oauth2/revoke"
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        body = {
		    'appkey': self.appkey,
		    'secretkey': self.secretkey,
		    'token': self.token,
	    }
        response = requests.post(url, headers=headers, json=body).json()


def _get_bearer(host: str, appkey: str, secretkey: str) -> str:
    url = f"{host}/oauth2/token"
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    body = {
        'grant_type': 'client_credentials',
        'appkey': appkey,
        'secretkey': secretkey,
    }
    response = requests.post(url, headers=headers, json=body).json()

    if response['return_code'] != 0:
        raise Exception(f'로그인 실패: {response['return_msg']}')
    
    return response['token']


