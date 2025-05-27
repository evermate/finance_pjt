# 프로젝트 README

## I. 팀원 정보 및 업무 분담 내역

| 이름      | 담당 업무                                                                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------- |
| **박민수** | - Vue.js를 활용한 프론트엔드 디자인<br>- UI/UX 설계 및 프론트엔드 총괄<br>- Kakao Maps API를 통한 은행까지 경로 탐색 기능 구현                       |
| **조영우** | - 금융 상품 가입 및 장바구니 담기 기능 구현<br>- 사용자 로그인 및 인증 시스템 구축<br>- 금융상품 추천 시스템 개발<br>- Kakao Maps API를 활용한 주변 은행 탐색 기능 구현 |
| **유태영** | - ChatGPT API를 활용한 상품 추천 로직 구현<br>- 사용자 자산 시뮬레이션 기능 개발<br>- 메인페이지 금융 뉴스 및 금융상품 카드 컴포넌트 구현                       |


## II. 설계 내용 및 실제 구현 정도

### 아키텍처 구성

본 프로젝트는 프론트엔드와 백엔드를 완전히 분리하여 RESTful API를 통해 통신하는 구조입니다.

* **Frontend**: Vue3, Pinia, Vue Router를 사용하여 화면 렌더링 및 사용자 입력 처리를 담당합니다.

  * Axios로 API 요청을 수행하여 데이터를 시각화합니다.

* **Backend**: Django와 Django REST Framework를 사용하여 인증, 금융상품 데이터 처리 및 추천 알고리즘을 구현했습니다.

  * 모든 응답은 JSON 형식으로 제공됩니다.

프론트엔드는 UI와 사용자 경험을, 백엔드는 데이터와 비즈니스 로직을 각각 명확히 분리하여 개발했습니다.

## III. 데이터베이스 모델링 (ERD)

![ERD](./docs/erd.png)

### ✅ 주요 모델 및 관계 구조

#### 1. **User**
- 기본 사용자 정보 저장
- `main_bank` 필드로 **Bank** 모델과 연결 (외래키)
- 사용자가 가입한 예적금 상품은 **JoinedProduct** 모델을 통해 연결

#### 2. **Bank**
- 고유 식별자: `fin_co_no`
- 예적금 상품(**DepositProduct**)과 연결 (1:N 관계)

#### 3. **DepositProduct**
- **Bank**와 연결 (외래키)
- 금리 옵션(**InterestOption**)과 연결 (1:N 관계)
- 사용자 가입(**JoinedProduct**)과 연결 (1:N 관계)

#### 4. **InterestOption**
- **DepositProduct**와 연결 (외래키)
- **JoinedProduct**를 통해 사용자와 간접적으로 연결됨

#### 5. **JoinedProduct**
- **User**, **DepositProduct**, **InterestOption**을 연결하는 중간 테이블
- `(user_id, option_id)`에 unique index 존재 → 동일 옵션 중복 가입 불가

#### 6. **Post**
- **User**와 연결 (작성자, 1:N 관계)
- 좋아요는 **post_likes**를 통해 사용자와 다대다 연결
- 댓글은 **Comment** 모델과 연결 (1:N 관계)

#### 7. **post_likes**
- **Post ↔ User** 다대다 연결용 테이블

#### 8. **Comment**
- **Post**, **User**와 연결 (외래키)
- `parent_id`를 통한 자기참조로 대댓글 구조 구현 가능


## IV. 금융 상품 추천 알고리즘에 대한 기술적 설명

### 금융상품 추천 로직

사용자의 연령과 자산 규모를 기반으로 맞춤형 금융 상품을 추천하는 알고리즘을 구현했습니다.

* **연령이 낮고 일정 수준 이상의 자산을 보유한 경우:**

  * 장기적이고 미래 지향적인 금융 상품을 추천하여 자산의 장기적인 성장을 지원합니다.
* **연령이 낮고 자산 규모가 크지 않은 경우:**

  * 비교적 짧은 기간 동안 자금을 쉽게 출금할 수 있는 단기 금융 상품을 추천합니다.
* **40세 이상 사용자:**

  * 자금 유출이 빈번하며 안정성을 중요시하는 경향을 고려하여 주요 4대 은행(KB국민은행, 신한은행, 우리은행, 하나은행)의 안정적인 단기 금융 상품을 우선적으로 추천합니다.

### 은퇴 자산 시뮬레이션 구현 (몬테카를로 시뮬레이션)

몬테카를로 시뮬레이션(Monte Carlo Simulation)은 불확실성이 존재하는 시스템이나 프로세스의 미래 동작을 확률적으로 예측하는 기법입니다. 본 프로젝트에서는 사용자의 은퇴 자산 관리 및 예측을 위해 해당 방법을 활용했습니다.

#### 몬테카를로 시뮬레이션 핵심 개념

* **난수 생성:**

  * 무작위로 선택된 값을 기반으로 다양한 시나리오를 생성하여 반복적으로 시스템의 동작을 시뮬레이션합니다.

* **확률 분포:**

  * 불확실성을 나타내는 변수들이 특정 확률 분포를 따르며, 이를 활용하여 투자 수익률, 금리, 물가 상승률과 같은 다양한 결과를 예측합니다.

* **반복적인 계산:**

  * 수많은 시뮬레이션을 반복 수행함으로써 시스템이 어떻게 변화할 수 있는지를 예측합니다. 각각의 시뮬레이션은 서로 다른 난수를 사용하여 독립적으로 수행되며, 최종적으로 평균 결과를 도출합니다.

* **결과 분석:**

  * 여러 번의 시뮬레이션 결과를 통해 도출된 데이터를 분석하여 불확실성을 파악하고, 이를 히스토그램이나 누적 분포 그래프 등으로 시각화하여 사용자가 쉽게 이해할 수 있도록 제공합니다.

#### 몬테카를로 시뮬레이션의 장점

* **불확실성 반영:** 다양한 변수의 불확실성을 반영해 보다 현실적이고 정확한 예측이 가능합니다.
* **다양한 시나리오 분석:** 최악에서 최상의 경우까지 모든 가능성을 고려하여 포괄적인 예측 결과를 제공합니다.
* **복잡한 문제 해결:** 수학적으로 해결하기 어려운 복잡한 문제를 근사적으로 해결할 수 있습니다.

#### 몬테카를로 시뮬레이션의 단점

* **시간 소모:** 많은 반복 계산이 필요하여 계산 시간이 길어질 수 있습니다.

## V. 서비스 대표 기능 설명

### 1. 예적금 금리 비교

* 금융상품 통합비교 API를 통해 예금과 적금 상품 데이터를 받아 DB에 저장하고, 사용자가 가입 기간 및 은행 선택을 통해 필터링된 상품 목록을 확인할 수 있도록 구성했습니다.
* 각 상품의 상세정보 조회 및 가입 기능을 제공합니다.

### 2. 금융 상품 추천 기능 

* 사용자의 연령과 자산 규모를 기반으로 맞춤형 금융 상품을 추천합니다.
* 은퇴 자산 예측을 위해 몬테카를로 시뮬레이션을 적용하여 다양한 미래 시나리오를 제공합니다.

### 3. 은퇴 자산 시뮬레이션 

* 사용자의 재정 계획(저축, 수익률, 지출 등)에 따라 은퇴 시점과 노후까지의 자산을 확률적으로 예측하여 시각화하여 제공합니다
* 주요 알고리즘은 몬테카를로 시뮬레이션으로, 미래 자산 변화의 불확실성을 반영해 다양한 시나리오를 분석합니다.

### 4. 근처 은행 검색

* Kakao Maps API를 이용하여 사용자가 선택한 위치 근처의 은행 정보를 지도에 시각적으로 표시합니다.
* 은행을 선택하면, 현재 위치에서 은행까지의 길을 표시합니다.

### 5. 현물 상품(금, 은) 가격 비교

* 금과 은의 가격 변동을 시각화한 차트를 제공하며, 특정 기간을 선택하면 해당 기간의 데이터만 표시됩니다.

### 6. 관심 종목 영상 검색

* Youtube API를 활용해 사용자가 입력한 검색어로 영상을 검색하고, 영상 목록 및 상세페이지를 제공합니다.

### 7. 커뮤니티 게시판

* 회원 간의 소통을 위한 게시판을 제공하며, 게시글 및 댓글 작성, 수정, 삭제는 작성자 본인만 가능합니다.

### 8. 프로필 페이지

* 사용자 정보 조회 및 수정 기능을 제공하며, 가입한 금융 상품 리스트와 금리 정보를 차트로 시각화하여 제공합니다.

## VI. 생성형 AI를 활용한 부분

- **ChatGPT API를 통한 금융상품 추천 로직 구현**
  - 사용자의 자산, 나이, 성향 등 다양한 입력 조건을 기반으로 AI가 문맥을 이해하고 자연어 기반의 추천 이유를 생성합니다.
  - 단순 알고리즘 추천이 아닌, 사용자에게 이해하기 쉬운 설명을 함께 제공함으로써 서비스의 신뢰성과 설득력을 강화했습니다.

- **코드 설계 및 문서화 지원**
  - 개발 초기 설계 단계에서 ChatGPT를 활용하여 ERD 작성, 모델 설계, 커밋 메시지 전략 수립 등 다양한 협업 도구로 활용했습니다.
  - 프론트엔드와 백엔드 통신 방식 설계에 있어서도 역할 분리 및 아키텍처 정리에 도움을 받았습니다.

---

## VII. 기타 (느낀 점, 후기 등)

- **협업의 가치**  
  처음부터 역할을 분담하고 API 명세를 명확히 정의함으로써 효율적인 협업이 가능했습니다. GitHub를 통한 버전 관리는 팀워크를 정립하는 데 큰 도움이 되었습니다.

- **기술 스택에 대한 실전 경험**  
  Django REST Framework와 Vue 3, Pinia, Kakao API, ChatGPT API 등의 기술들을 프로젝트에 직접 적용해보며 깊은 이해를 얻었습니다.

- **후속 목표**  
  향후에는 추천 모델의 고도화, 실거래 데이터 연동, 사용자 피드백 기반 개선 등을 통해 서비스의 실용성과 현실 적용 가능성을 더 높이고 싶습니다.


## VIII. 커밋 메시지 컨벤션

| 타입         | 설명                 |
| ---------- | ------------------ |
| `feat`     | 새로운 기능 추가          |
| `fix`      | 버그 수정              |
| `docs`     | 문서 수정 (README 등)   |
| `refactor` | 코드 리팩토링 (기능 변화 없음) |
| `style`    | 코드 스타일 수정          |
| `test`     | 테스트 코드 추가 및 수정     |
| `chore`    | 빌드 및 설정 관련 작업      |

예시:

```
feat: 로그인 기능 추가  
fix: 회원가입 오류 수정  
docs: README 업데이트  
refactor: 중복 코드 리팩토링  
style: 들여쓰기 수정  
test: 로그인 테스트 코드 추가  
chore: requirements.txt 업데이트 
```

## IX. 사용 흐름

1. 프로젝트를 클론합니다.

```bash
git clone https://github.com/your-team/final_pjt.git
cd final_pjt
```

2. `.env.example` 파일을 참고하여 `.env` 파일을 설정합니다.

3. 백엔드 환경 설정 및 실행

```bash
cd backend
python -m venv venv
source venv/bin/activate  # (Windows는 venv\Scripts\activate)
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 예적금 상품 데이터 수집
python manage.py collect_deposit

# 더미 데이터 적재
python manage.py load_fixtures
```

4. 프론트엔드 환경 설정 및 실행

```bash
cd ../frontend
npm install
npm run dev
```

5. 설정이 완료되면 프론트엔드 및 백엔드 서버를 각각 실행합니다.

## X. 파일 구조

```
final_pjt
├─ backend
│  ├─ accounts
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ migrations
│  │  ├─ models.py
│  │  ├─ serializers.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  ├─ api
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ migrations
│  │  ├─ models.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views
│  │  │  ├─ map_search.py
│  │  │  ├─ video_detail.py
│  ├─ backend
│  │  ├─ asgi.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  ├─ wsgi.py
│  ├─ community
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ migrations
│  │  ├─ models.py
│  │  ├─ serializers.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  ├─ fixtures
│  │  ├─ comments_fixture.json
│  │  ├─ joined_products_fixture.json
│  │  ├─ posts_fixture.json
│  │  ├─ post_likes_fixture.json
│  │  └─ users_fixture.json
│  ├─ manage.py
│  ├─ products
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ management
│  │  │  ├─ commands
│  │  │  │  ├─ collect_deposit.py
│  │  │  │  ├─ generate_fixtures.py
│  │  │  │  ├─ init_dummy.py
│  │  │  │  ├─ load_fixtures.py
│  │  ├─ migrations
│  │  ├─ models.py
│  │  ├─ serializers.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views
│  │  │  ├─ ai_recommendation.py
│  │  │  ├─ main.py
│  │  │  ├─ recommendation.py
│  ├─ requirements.txt
│  └─ simulation
│     ├─ admin.py
│     ├─ apps.py
│     ├─ migrations
│     ├─ models.py
│     ├─ serializers.py
│     ├─ tests.py
│     ├─ urls.py
│     ├─ utils.py
│     ├─ views.py
├─ docs
│  └─ erd.png
├─ frontend
│  ├─ .editorconfig
│  ├─ .prettierrc.json
│  ├─ eslint.config.js
│  ├─ image
│  │  ├─ community.jpg
│  │  ├─ compare_pic.png
│  │  ├─ compare_pic2.jpg
│  │  ├─ compare_pic3.jpg
│  │  ├─ Compass.png
│  │  ├─ Database.png
│  │  ├─ goldbar.jpg
│  │  ├─ LinkedIn.png
│  │  ├─ Logo Instagram.png
│  │  ├─ Logo YouTube.png
│  │  ├─ MainLogo.png
│  │  ├─ MainLogo1.png
│  │  ├─ map.jpg
│  │  ├─ marker_selected_custom.png
│  │  ├─ no-data.jpg
│  │  ├─ notebook.jpg
│  │  ├─ recommend.jpg
│  │  ├─ Search.png
│  │  ├─ search2.jpg
│  │  ├─ simulation.jpg
│  │  ├─ User.png
│  │  ├─ wealth_simulation.png
│  │  └─ weighing-scale.png
│  ├─ index.html
│  ├─ jsconfig.json
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
│  │  ├─ bank-icons
│  │  │  ├─ default.png
│  │  │  ├─ gookmin.png
│  │  │  ├─ gwangju_jungbook.png
│  │  │  ├─ gyungnam_busan.png
│  │  │  ├─ hana.png
│  │  │  ├─ ibk_giup.png
│  │  │  ├─ imbank.png
│  │  │  ├─ kakao.png
│  │  │  ├─ kbank.png
│  │  │  ├─ kdb_sanup.png
│  │  │  ├─ nonghyup.png
│  │  │  ├─ scjeil.png
│  │  │  ├─ shinhan_jeju.png
│  │  │  ├─ soohyup.png
│  │  │  ├─ toss.png
│  │  │  └─ woori.png
│  │  ├─ bank-icons-long
│  │  │  ├─ default.png
│  │  │  ├─ long_busanbank.png
│  │  │  ├─ long_gookmin.png
│  │  │  ├─ long_gwangju.png
│  │  │  ├─ long_gyungnam.png
│  │  │  ├─ long_hana.png
│  │  │  ├─ long_ibk_giup.png
│  │  │  ├─ long_imbank.png
│  │  │  ├─ long_jeju.png
│  │  │  ├─ long_jungbook.png
│  │  │  ├─ long_kakao.png
│  │  │  ├─ long_kbank.png
│  │  │  ├─ long_kdb_sanup.png
│  │  │  ├─ long_nonghyup.png
│  │  │  ├─ long_scjeil.png
│  │  │  ├─ long_shinhan.png
│  │  │  ├─ long_soohyup.png
│  │  │  ├─ long_toss.png
│  │  │  └─ long_woori.png
│  │  ├─ dummy
│  │  │  └─ news
│  │  │     ├─ chaegwuan.jpg
│  │  │     ├─ LGUplus_AI.jpg
│  │  │     ├─ noin_hire.jpg
│  │  │     ├─ openai.jpg
│  │  │     └─ samsung_bespoke.jpg
│  │  └─ favicon.ico
│  ├─ README.md
│  ├─ src
│  │  ├─ App.vue
│  │  ├─ assets
│  │  │  ├─ data.js
│  │  │  ├─ loading1.png
│  │  │  └─ loading2.png
│  │  ├─ components
│  │  │  ├─ AiReport.vue
│  │  │  ├─ CommentItem.vue
│  │  │  ├─ ConfirmModal.vue
│  │  │  ├─ Eda
│  │  │  │  ├─ InfographicSection.vue
│  │  │  │  ├─ MiniChart.vue
│  │  │  │  ├─ NewsBoard.vue
│  │  │  │  └─ NewsDetailModal.vue
│  │  │  ├─ HeaderNav.vue
│  │  │  ├─ JoinedProductsChart.vue
│  │  │  ├─ LoadingSpinner.vue
│  │  │  ├─ MyProductsPanel.vue
│  │  │  ├─ ProductCard.vue
│  │  │  ├─ ProductSlider.vue
│  │  │  ├─ SimulationChart.vue
│  │  │  └─ SimulationForm.vue
│  │  ├─ constants.js
│  │  ├─ data
│  │  │  ├─ dummy
│  │  │  │  └─ news.js
│  │  │  └─ infographicData.js
│  │  ├─ excel
│  │  │  ├─ Gold_prices.json
│  │  │  └─ Silver_prices.json
│  │  ├─ main.js
│  │  ├─ stores
│  │  │  ├─ accounts.js
│  │  │  ├─ comment.js
│  │  │  ├─ community.js
│  │  │  ├─ modal.js
│  │  │  ├─ recommend.js
│  │  │  └─ simulation.js
│  │  ├─ utils
│  │  └─ views
│  │     ├─ community
│  │     │  ├─ CommunityDetailView.vue
│  │     │  ├─ CommunityFormView.vue
│  │     │  ├─ CommunityListView.vue
│  │     │  └─ UserProfileView.vue
│  │     ├─ CompareView.vue
│  │     ├─ HomeView.vue
│  │     ├─ LoginView.vue
│  │     ├─ MapView copy.vue
│  │     ├─ MapView.vue
│  │     ├─ MyPageEdit.vue
│  │     ├─ MyPageView.vue
│  │     ├─ PricesView.vue
│  │     ├─ product
│  │     │  └─ DepositDetailView.vue
│  │     ├─ RecommendView.vue
│  │     ├─ SearchView.vue
│  │     ├─ SignUp.vue
│  │     ├─ SimulationView.vue
│  │     └─ VideoDetailView.vue
│  └─ vite.config.js
└─ README.md

```