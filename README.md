# Economic Trend Observation System Platform

지정학적 뉴스는 제외하고 공급·수요, 자금 흐름, 투자심리의 모순과 가격 확인을 이용해 경제 흐름과 바닥 후보를 관찰하는 Railway용 초기 프로젝트입니다.

## 구성

- FastAPI 웹 대시보드
- PostgreSQL 리포트 저장
- 평일 데일리 리포트 생성 작업
- ECOS·FRED 데이터 클라이언트
- TradingView 차트 바로가기
- 미국·일본·중국·한국 4개국 비교 분석
- 한국 수출·내수·가계부채·외국인 수급 심층분석
- 100점 후보 평가 엔진

## 로컬 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

브라우저에서 `http://localhost:8000`을 엽니다.

## Railway 배포

1. Railway 프로젝트에 PostgreSQL을 추가합니다.
2. 이 GitHub 저장소를 Web Service로 연결합니다.
3. Variables에 `DATABASE_URL`, `ECOS_API_KEY`, `FRED_API_KEY`를 설정합니다.
4. Web Service 시작 명령은 다음과 같습니다.

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. 같은 저장소를 Cron Service로 한 번 더 추가합니다.
6. Cron 시작 명령은 `python -m jobs.daily_report`로 설정합니다.
7. Railway Cron은 UTC 기준입니다. 평일 한국시간 오전 9시 40분은 `40 0 * * 1-5`입니다.

## 검수된 리포트 게시

`data/reports/YYYY-MM-DD.json` 파일을 GitHub에 추가하면 Railway 재배포 시 자동으로 PostgreSQL에 등록됩니다. 같은 날짜의 파일을 수정해 다시 푸시하면 해당 날짜 리포트가 갱신됩니다. 메인 화면에는 최신 리포트가, `/history`에는 날짜별 기록이 표시됩니다.

## 점수 기준

| 영역 | 배점 |
|---|---:|
| 공급·수요 | 25 |
| 자금 흐름 | 20 |
| 심리의 모순 | 20 |
| 바닥 확인 | 20 |
| 재무 안전성 | 15 |

70점 이상은 관찰 후보, 80점 이상이면서 가격 확인 조건을 충족하면 확인 후보입니다. 이 서비스는 투자 권유가 아니라 데이터 관찰 도구입니다.
