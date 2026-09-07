COUNTRY_PROFILES = {
    "KR": {
        "code": "KR", "name": "한국", "detail": True,
        "summary": "수출·반도체·내수·가계부채·원화·외국인 수급을 함께 봅니다.",
        "indicators": [
            ("KOSPI", "KRX:KOSPI", "시장 위험선호"),
            ("KOSDAQ", "KRX:KOSDAQ", "중소형 성장주 심리"),
            ("원·달러", "FX_IDC:USDKRW", "외국인 자금과 수입물가"),
            ("한국 10년물", "TVC:KR10Y", "장기 조달비용"),
            ("삼성전자", "KRX:005930", "반도체·수출 대표"),
            ("SK하이닉스", "KRX:000660", "메모리 수요 선행"),
        ],
        "sections": [
            ("수출 엔진", "반도체 수출, 전체 수출, 일평균 수출, 무역수지"),
            ("내수 체력", "소매판매, 서비스업 생산, 소비자심리, 카드 사용"),
            ("기업 자금", "회사채 스프레드, 기업대출, 부도율, 설비투자"),
            ("가계와 부동산", "가계대출, 주택거래, 전세·매매가격, 연체율"),
            ("외국인 수급", "코스피 순매수, 원화, 반도체 비중, 선물 포지션"),
            ("물가와 금리", "CPI, 생산자물가, 기준금리, 국고채 금리"),
        ],
    },
    "US": {
        "code": "US", "name": "미국", "detail": False,
        "summary": "고용·물가·소비·신용·달러 유동성이 세계 자금 흐름을 결정합니다.",
        "indicators": [("S&P 500", "SP:SPX", "대형주 위험선호"), ("Nasdaq 100", "NASDAQ:NDX", "성장주 유동성"), ("미국 2년물", "TVC:US02Y", "정책금리 기대"), ("미국 10년물", "TVC:US10Y", "장기 할인율"), ("달러지수", "TVC:DXY", "세계 달러 유동성"), ("VIX", "CBOE:VIX", "주식 변동성")],
        "sections": [("성장", "GDP·소비·ISM"), ("고용", "비농업고용·실업률·임금"), ("물가", "CPI·PCE·생산자물가"), ("유동성", "연준 자산·M2·신용스프레드")],
    },
    "JP": {
        "code": "JP", "name": "일본", "detail": False,
        "summary": "엔화·일본은행·임금·수출기업 이익의 연결을 봅니다.",
        "indicators": [("Nikkei 225", "TVC:NI225", "대형 수출주"), ("TOPIX", "TSE:TOPIX", "일본 시장폭"), ("달러·엔", "FX:USDJPY", "수출 채산성과 자금 이동"), ("일본 10년물", "TVC:JP10Y", "BOJ 정상화 압력")],
        "sections": [("통화", "BOJ·국채금리·엔화"), ("임금과 물가", "춘투·실질임금·CPI"), ("기업", "수출·설비투자·기업지배구조")],
    },
    "CN": {
        "code": "CN", "name": "중국", "detail": False,
        "summary": "부동산·신용·제조업 수요·위안화와 정책 유동성을 봅니다.",
        "indicators": [("상하이종합", "SSE:000001", "본토 위험선호"), ("CSI 300", "SSE:000300", "대형 우량주"), ("홍콩 항셍", "TVC:HSI", "외국자금 심리"), ("달러·위안", "FX_IDC:USDCNY", "자본유출 압력")],
        "sections": [("신용", "사회융자총량·대출·M2"), ("부동산", "거래·가격·착공"), ("제조업", "PMI·산업생산·수출"), ("내수", "소매판매·소비심리")],
    },
}


# 국가별 대표성과 거래 유동성을 기준으로 고정한 관찰 종목입니다.
# 가격과 수익률은 매일 생성되는 리포트의 top_stocks 데이터로 덮어씁니다.
TOP_STOCKS = {
    "KR": [
        ("삼성전자", "KRX:005930"), ("SK하이닉스", "KRX:000660"), ("LG에너지솔루션", "KRX:373220"), ("삼성바이오로직스", "KRX:207940"),
        ("현대차", "KRX:005380"), ("기아", "KRX:000270"), ("KB금융", "KRX:105560"), ("NAVER", "KRX:035420"),
        ("한화에어로스페이스", "KRX:012450"), ("HD현대중공업", "KRX:329180"), ("셀트리온", "KRX:068270"), ("신한지주", "KRX:055550"),
        ("삼성물산", "KRX:028260"), ("POSCO홀딩스", "KRX:005490"), ("현대모비스", "KRX:012330"), ("삼성생명", "KRX:032830"),
        ("카카오", "KRX:035720"), ("SK스퀘어", "KRX:402340"), ("두산에너빌리티", "KRX:034020"), ("삼성SDI", "KRX:006400"),
    ],
    "US": [
        ("NVIDIA", "NASDAQ:NVDA"), ("Microsoft", "NASDAQ:MSFT"), ("Apple", "NASDAQ:AAPL"), ("Amazon", "NASDAQ:AMZN"),
        ("Alphabet", "NASDAQ:GOOGL"), ("Meta Platforms", "NASDAQ:META"), ("Broadcom", "NASDAQ:AVGO"), ("Tesla", "NASDAQ:TSLA"),
        ("Berkshire Hathaway", "NYSE:BRK.B"), ("JPMorgan Chase", "NYSE:JPM"), ("Walmart", "NYSE:WMT"), ("Eli Lilly", "NYSE:LLY"),
        ("Visa", "NYSE:V"), ("Exxon Mobil", "NYSE:XOM"), ("Mastercard", "NYSE:MA"), ("Netflix", "NASDAQ:NFLX"),
        ("Costco", "NASDAQ:COST"), ("Oracle", "NYSE:ORCL"), ("Palantir", "NASDAQ:PLTR"), ("AMD", "NASDAQ:AMD"),
    ],
    "JP": [
        ("Toyota Motor", "TSE:7203"), ("Mitsubishi UFJ", "TSE:8306"), ("Sony Group", "TSE:6758"), ("Hitachi", "TSE:6501"),
        ("SoftBank Group", "TSE:9984"), ("Nintendo", "TSE:7974"), ("Keyence", "TSE:6861"), ("Recruit Holdings", "TSE:6098"),
        ("Fast Retailing", "TSE:9983"), ("Sumitomo Mitsui FG", "TSE:8316"), ("Tokyo Electron", "TSE:8035"), ("Mizuho FG", "TSE:8411"),
        ("NTT", "TSE:9432"), ("Mitsubishi Corp", "TSE:8058"), ("Itochu", "TSE:8001"), ("Advantest", "TSE:6857"),
        ("Honda Motor", "TSE:7267"), ("Shin-Etsu Chemical", "TSE:4063"), ("Daiichi Sankyo", "TSE:4568"), ("Tokyo Marine", "TSE:8766"),
    ],
    "CN": [
        ("Tencent", "HKEX:700"), ("Alibaba", "HKEX:9988"), ("Kweichow Moutai", "SSE:600519"), ("ICBC", "SSE:601398"),
        ("China Construction Bank", "SSE:601939"), ("BYD", "SZSE:002594"), ("CATL", "SZSE:300750"), ("China Mobile", "SSE:600941"),
        ("Agricultural Bank of China", "SSE:601288"), ("PetroChina", "SSE:601857"), ("Ping An Insurance", "SSE:601318"), ("Bank of China", "SSE:601988"),
        ("PDD Holdings", "NASDAQ:PDD"), ("Meituan", "HKEX:3690"), ("Xiaomi", "HKEX:1810"), ("China Merchants Bank", "SSE:600036"),
        ("JD.com", "HKEX:9618"), ("NetEase", "HKEX:9999"), ("Baidu", "HKEX:9888"), ("Li Auto", "HKEX:2015"),
    ],
}
