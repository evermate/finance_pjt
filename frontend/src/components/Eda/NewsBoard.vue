<template>
  <section class="news-board">
    <h2 style="text-align: left;">최신 금융 뉴스</h2>

    <!-- 탭 -->
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.value===null?'all':tab.value"
        :class="['tab', { active: selectedTab === tab.value }]"
        @click="selectTab(tab.value)"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 검색 (옵션) -->
    <div class="search-bar">
      <input v-model="searchKeyword" @keyup.enter="handleSearch" placeholder="검색어를 입력하세요" />
      <button @click="handleSearch">검색</button>
    </div>

    <!-- 게시판 테이블 -->
    <table class="board-table">
      <thead>
        <tr>
          <th>번호</th>
          <th>제목</th>
          <th>글쓴이</th>
          <th>날짜</th>
          <th>조회수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in filteredPosts" :key="post.id">
          <td>{{ post.id }}</td>
          <td class="title-cell">
            <span :class="['badge', post.category]">{{ categoryLabel(post.category) }}</span>
            <a href="javascript:;" @click="openDetail(post)">{{ post.title }}</a>
          </td>
          <td>{{ post.author }}</td>
          <td>{{ post.date }}</td>
          <td>{{ post.views }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 글쓰기 버튼 -->
    <!-- <div class="write-btn">
      <RouterLink to="/community/write">
        <button>글쓰기</button>
      </RouterLink>
    </div> -->

    <!-- ── 여기에 상세 모달 컴포넌트 넣어 주기 ── -->
    <NewsDetailModal
      :visible="showDetail"
      :post="currentPost"
      @close="showDetail = false"
    />
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import NewsDetailModal from './NewsDetailModal.vue'

const tabs = [
  // { label: '전체',           value: null   },
  // { label: '금융상품 리뷰', value: 'review' },
  // { label: '주요 뉴스',     value: 'news'   },
  // { label: '자유 게시판',   value: 'free'   },
]

const selectedTab = ref(null)
const searchQuery = ref('')
const showDetail = ref(false)
const currentPost = ref({})

// 예시 데이터 (실제 API 연동하셔도 됩니다)
// src/components/NewsBoard.vue
const posts = ref([
  {
    id:       5,
    category: 'news',
    title:    '오픈AI의 선택',
    author:   'forrest_gump',
    date:     '5월 27일 오후 02:43',
    views:    0,
    image:    '/article-imgs/openai.jpg',
    body:     '이 신제품은 메세지모찌라는 이름답게 …',
    content:  '미국 샌프란시스코 공항에 내려 시내로 이동하는 동안 수많은 대형 광고판을 보게 되는데, 몇 년 전부터 이 광고판들은 AI 광고로 도배가 되어있다. 일레븐랩스처럼 AI 기업의 광고는 물론이고, 세일즈포스처럼 기업용 솔루션 업체의 AI 서비스 광고까지, 온통 AI 얘기밖에 없다. 그 열기는 인터넷이 보급되던 시절을 생각나게 한다. 챗GPT로 AI 경쟁의 선두에 있는 오픈AI의 고민이 여기에 있다. 모두가 AI를 하겠다고 하는 세상에서 가장 인기있는 챗봇을 가진 것만으로는 살아남기 힘들다. 당장 구글만 해도 이번 I/O 행사에서 자사의 제미나이 AI를 구글 서비스 전반에 적용하는 야심찬 계획을 발표했다. 이 상황을 1990년대 최고의 인기 웹브라우저였던 넷스케이프에 비유하기도 한다. 넷스케이프는 성능이 뛰어났지만, 마이크로소프트가 장악한 PC 생태계에서 웹브라우저만으로 살아남기는 힘들었다. 오픈AI가 피하려는 것이 바로 넷스케이프의 운명이다. 하나의 뛰어난 서비스만을 가진 기업은 실리콘밸리에서 오래 생존하기 힘들다. 무엇보다 오픈AI가 받은 천문학적 투자액은 투자자들이 아주 큰 그림을 요구하고 있음을 의미한다. 인기 챗봇을 넘어 AI를 기반으로 한 플랫폼을 구축하고, 그걸로 구글, 아마존, 메타와 경쟁하라는 것. 지난주 오픈AI가 애플의 전설적인 디자이너 조니 아이브의 AI 기기 개발 스타트업 아이오(io)를 우리 돈 9조원에 가까운 가격에 인수한 이유도 여기에 있다. 사용자와 직접 만나는 접점이 없이 폰이나 웹브라우저와 같은 다른 기업의 플랫폼에 올라타서 사업을 확장하는 데는 분명한 한계가 있기 때문이다. 한 전문기자는 “오픈AI의 목표는 넷스케이프가 아니라, 구글이 되는 것”이라고 했다. 검색 엔진이라는 하나의 인기 서비스로 출발해서 거대 플랫폼이 된 좋은 예이기 때문이다.'
  },
  {
    id:       4,
    category: 'news',
    title:    '‘노인 고용률 1위’ 이면엔···65세 3명 중 1명 단순노무직',
    author:   'forrest_gump',
    date:     '5월 27일 오후 02:43',
    views:    0,
    image:    '/article-imgs/noin_hire.jpg',
    body:     '이 신제품은 메세지모찌라는 이름답게 …',
    content:  '한국의 65세 이상 노인 고용률이 경제협력개발기구(OECD) 회원국 중 1위이지만, 65세 노인 3명 중 1명은 단순노무직에 종사하는 등 고령층 일자리의 질은 낮은 것으로 나타났다. 연금 소득이 최저 생계비에도 미치지 못해 은퇴할 수 없는 노인들은 재취업에 성공하더라도 상당수가 영세한 사업장에서 비정규직으로 저숙련·단순노동을 하고 있다는 것이다. 27일 국회 예산정책처의 ‘고령층의 경제활동 실태 및 소득공백’ 보고서를 보면, 2023년 기준 한국 65세 이상 인구의 고용률은 37.3%로 OECD 국가 중 가장 높았다. OECD 평균(13.6%)의 3배 가까이 높고, 초고령화 국가인 일본(25.3%)보다도 10%포인트 이상 높다. 보고서는 한국의 노인 고용률이 높은 이유로 최저 생계비에도 못 미치는 ‘부족한 연금 소득’을 꼽았다. 연금 소득만으로 생계를 꾸리기 어렵기 때문에 은퇴를 하지 못한다는 뜻이다. 65세 이상 연금소득자의 월평균 연금소득은 약 80만원으로, 2024년 기준 1인 가구 월 최저생계비(134만원)보다 낮다. 문제는 노인 일자리가 수요 대비 충분하지 않다는 점이다. 지난해 65세 노인 중 장래 계속 일하기를 희망하는 비중은 73.5%였으나 실제 취업자 비중은 56.7%에 그쳤다. 고령층이 취업하더라도 일자리의 질은 낮았다. 65세 임금노동자 중 61.2%는 비정규직이었다. 절반 가량(49.4%)은 10인 미만 영세사업체에서 일했다. 직업 유형별로는 단순노무직 비중이 35.4%로 가장 많았고 서비스직(15.3%), 기계조작원(15.0%)이 뒤를 이었다. 단순 노무직의 비중은 연령이 높아질수록 늘어나 70세 일자리의 60.5%가 단순 노무직이었다. 나이를 들수록 임금은 하락했다. 지난해 65세 임금노동자는 월평균 임금 221만원을 받았지만, 70세는 160만원을 받는 데 그쳤다. 보고서는 고령층 임금이 줄어든 주요 원인으로 정규직 일자리 이탈과 노인 ‘경력 단절’을 꼽았다. 지난해 기준 생애 주된 일자리에서 퇴직한 55~70세 인구의 퇴직 당시 평균 연령은 51.2세였다. 연금 수급 연령까지 소득 공백이 생기게 된 것이다. 다른 일자리를 찾아 재취업한 65세 이상 임금노동자 중 현재 일자리가 생애 주된 일자리와 ‘전혀’ 또는 ‘별로’ 관련 없다고 응답한 비중은 53.2%에 달했다. 60~64세 인구 중 생애 주된 일자리에서 60세까지 무사히 근무하고 정년퇴직한 비중은 5명 중 1명에 불과했다. 이들 정년퇴직자의 과반수(53.4%)는 화이트 칼라였다. 정년퇴직자들의 월평균 연금액은 183만~210만원으로 같은 연령대 연금소득자 평균인 109만원보다 2배 가까이 많았다. 보고서는 “고령층이 생애 주된 일자리 또는 그와 관련성 높은 일자리에 오래 머물도록 지원하는 것은 노년기 소득 공백 완화와 더불어 근로자의 인적 자본 활용 차원에서 의미가 있다”며 “생애 주요 경력이 단절되는 고령층의 재취업 지원 및 일자리 미스매치 해소 방안을 모색해야 한다”고 촉구했다.'
  },
  {
    id:       3,
    category: 'news',
    title:    '일본 국채금리 뛰며 자금 이동 조짐…국채 시장 급랭 가능성',
    author:   'forrest_gump',
    date:     '5월 27일 오후 02:46',
    views:    0,
    image:    '/article-imgs/chaegwuan.jpg',   // ← 여기에 이미지 URL
    body:     '다가오는 금요일, 전격 이벤트가 공개됩니다. 이번 행사에서는 …',    // ← 요약이나 본문 텍스트
    content:  '<strong>‘부채 포비아’에 흔들리는 안전자산 국채 </strong> \n 글로벌 국채 시장이 녹아내리고 있다. 빚에 취한 정부가 쏟아내는 국채에 대한 투자자의 너그러움이 사라지면서다. 장기물을 중심으로 수요가 줄면서 채권값은 하락하고 금리는 치솟고 있다. 대표적인 안전 자산으로 여겨졌던 국채의 위기다. 조짐은 이미 있었다. 도널드 트럼프 미국 대통령이 주도하는 관세 전쟁이 격화하며 지난달 초 벌어진 투매로 세계 금융 시장은 "국채 발작"을 겪었다. 미국에 상품 등을 수출해 무역흑자를 낸 국가가 미국 국채를 사들이며 낮은 국채 금리를 유지하는 "달러 리사이클링" 구조가 관세 폭탄으로 인해 무너질 수 있다는 우려 때문이었다. 미 국채 금리는 일제히 치솟고 달러 가치도 내려앉았다. 그러자 트럼프 대통령이 서둘러 상호관세 90일 유예 카드를 꺼내들었고, 시장도 안정을 찾는가 싶었다. 그러나 투자자의 인내심은 오래가지 않았다. 지난 21일 미국 20년물과 30년물 금리가 모두 심리적 저항선으로 여겨지는 5%를 돌파했다. 30년물 금리는 장중 한때 5.1%에 육박하며 2023년 11월 이후 1년 6개월 만에 가장 높은 수준을 기록했다. 트럼프가 대규모 감세안(메가 법안) 통과를 위해 공화당내 반대파에 대한 설득과 압박에 나선 데다, 이날 미 재무부가 진행한 국채 20년물 입찰에서 응찰률이 부진했던 탓이다. 흔들린 시장은 미국만이 아니다. 이날 일본 국채 시장도 요동쳤다. 일본 국채 30년물과 40년물 국채 금리가 최고치로 치솟았다. 장중 한때 30년물 금리는 3.185%, 40년물 금리는 3.635%까지 뛰었다. 20년물 금리도 2000년 10월 이후 가장 높은 2.575%까지 상승했다. 미국처럼 부진한 국채 입찰이 금리를 끌어올린 기폭제가 됐다. 전날(20일) 진행된 일본 재무성의 20년 만기 국채 입찰에서 평균 낙찰가와 최저 낙찰가 차이는 1987년 이후 38년 만에 가장 크게 벌어졌다. 최고 낙찰금리(연 2.54%)는 1999년 7월 이후 26년 만에 가장 높았다. 독일과 영국 등의 장기 국채 금리도 뛰었다.\n \n <strong>채권 리스크 프리미엄 더 높이는 시장</strong> \n로이터는 “장기 국채 금리 상승과 국채 입찰 부진은 투자자가 각국 정부에 던지는 명확한 메시지”라며 “최근의 불확실성 속에 몇십 년간 돈을 빌리려면 더 많은 이자를 줘야 한다는 것”이라고 지적했다. 취리히 보험 그룹의 수석 시장전략가인 가이 밀러는 로이터와의 인터뷰에서 “투자자 입장에선 부채가 계속 악화하고 성장 동력이 보다 취약한 세상이라면 채권을 보유하기 위해 요구하는 리스크 프리미엄이 더 높아져야 한다고 생각하는 것”이라고 말했다.'
  },
  {
    id:       2,
    category: 'news',
    title:    'LG유플러스가 ‘AI 상담 어드바이저’로 아낀 시간은 “월 117만분”',
    author:   'forrest_gump',
    date:     '5월 27일 오후 02:43',
    views:    0,
    image:    '/article-imgs/LGUplus_AI.jpg',
    body:     '이 신제품은 메세지모찌라는 이름답게 …',
    content:  'LG유플러스가 고객 질문을 이해하고 맞춤형 상담 내용을 상담사에게 추천하는 ‘인공지능(AI) 상담 어드바이저’ 도입으로 전체 상담 시간을 월평균 약 117만분 단축한 것으로 나타났다. LG유플러스는 27일 서울 용산구 사옥에서 기자간담회를 열고 “지난해 9월 자체 개발한 AI 상담 어드바이저를 자사 고객센터에 도입한 이후 전체 상담 시간이 19% 개선됐다”고 밝혔다. 통화당 연결 대기 시간은 평균 17초, 통화 시간은 평균 30초 줄었다. 평일 하루 평균 7만5000여건의 상담이 접수된다는 점을 고려하면 한 달 간 약 117만분에 달하는 고객의 시간을 아낀 것으로 분석된다고 회사는 전했다. AI 상담 어드바이저는 상담사가 고객 전화를 받는 순간부터 상담 종료 후 처리해야하는 일까지 전 과정을 지원하는 AI 에이전트다. 상담사가 보는 화면에 음성 대화 내용을 곧장 텍스트로 보여준다. 동시에 대화 맥락에 맞는 적절한 상담 정보를 추천한다. 전화를 끊은 뒤 상담 주제를 분류하는 작업까지 대신해준다. 서남희 LG유플러스 CV(고객가치) 담당은 “현장에선 후처리 업무를 하지 않아도 않다는 점에서 만족도가 높다”며 “여력이 생기니 다음 전화를 더 빨리 받을 수 있게 되는 것”이라고 말했다. 기존 콜센터 운영 방식에서 벗어나 AI를 활용해 고객을 응대하는 ‘AI컨택센터(AICC)’ 도입이 빨라지고 있다. 시장조사업체 얼라이드마켓리서치에 따르면 국내 AICC 시장은 연평균 23.7% 성장해 2030년 약 4546억원 규모에 이를 것으로 전망된다. 정성권 LG유플러스 IT·플랫폼빌드그룹장은 “AI 시대에도 인간 상담사의 응대 능력은 고객 만족에서 매우 중요한 역할을 하고 있다”며 AI 상담 어드바이저 개발 배경을 설명했다. 핵심 기술 중 하나는 AI가 스스로 상담 상황을 파악해 기업 내부 정보를 검색하고 답변을 생성하는 ‘에이전트 래그(RAG)’다. 예를 들어 고객이 “이심(eSIM)이 뭐냐”고 물으면 설명에 더해 가입 절차와 주의사항까지 제시한다. 자체 분석 결과 답변 정확도는 90%에 달했다. AI의 상담 주제 분류가 정확한지를 또 다른 AI 엔진으로 검증하고, 틀릴 경우 스스로 학습해 수정하는 ‘AI 인 더 루프(Loop)’ 기술도 적용됐다. 회사는 AI가 상담 내용을 일관된 방식으로 평가하고 피드백을 제공하는 ‘AI 오토 QA’도 이르면 6월 도입한다. 기술 고도화를 통해 전체 상담 시간 감소율을 30%로 끌어올릴 계획이다. 정 그룹장은 “지금은 자체 고객센터에서만 상담 어드바이저를 사용하고 있지만 기업 대상으로 상품화하는 작업도 진행하고 있다”고 말했다.'
  },
  {
    id:       1,
    category: 'news',
    title:    '삼성전자, ‘비스포크 AI 에어 콤보’ 출시',
    author:   'forrest_gump',
    date:     '5월 27일 오후 02:43',
    views:    0,
    image:    '/article-imgs/samsung_bespoke.jpg',
    body:     '“내 이름은 포레스트 검프”라는 영화 속 주인공 이야기…',
    content:  '삼성전자는 공조시스템 ‘비스포크 AI 에어 콤보’(사진)를 새롭게 선보였다. 가정용 시스템에어컨과 연결해 주거용 통합 공조시스템을 완성하는 환기용 기기다. 실내 오염된 공기를 흡입해 방출하고, 습도·이산화탄소·미세먼지 등을 걸러낸 쾌적한 외부 공기를 거실과 방뿐만 아니라 에어컨이 없는 실내 구석구석까지 공급한다. 특히, ‘정온제습모듈’을 탑재해 공간의 습도까지 최적으로 케어한다. 하루 최대 32L 대용량을 제습할 수 있는 우수한 성능으로 실내 구석구석의 습도를 조절한다. 별도 배관으로 습기를 배출하기 때문에 물통을 비울 필요도 없다. 또 ▲입자가 큰 먼지를 제거하는 극세 필터 ▲초미세먼지를 제거하고 세균 증식을 억제하는 항균 처리 집진 필터 ▲열교환기를 관리하는 워시클린 ▲바람을 만드는 팬까지 살균하는 UV-C FAN 살균 기능 등 4단계 클린 케어 시스템을 갖췄다. ‘비스포크 AI 에어 콤보’는 전국 500여 개 삼성스토어와 삼성닷컴에서 2025년 3월 이후 출시된 삼성전자 가정용 시스템에어컨과 함께 구매할 수 있다.'
  }
])

// 탭 선택
function selectTab(val) {
  selectedTab.value = val
}

// 검색 (임시 필터)
function onSearch() {
  // 간단히 searchQuery가 제목에 포함된 것만 보여주도록
  // 필요 없으면 지우셔도 됩니다
}

// 각 카테고리의 한글 레이블
function categoryLabel(cat) {
  switch(cat) {
    case 'review': return '리뷰'
    case 'news':   return '뉴스'
    case 'free':   return '자유'
    default:       return ''
  }
}

// 실제로 테이블에 뿌릴 데이터
const filteredPosts = computed(() => {
  let list = posts.value.slice().sort((a,b)=>b.id-a.id)
  if (selectedTab.value) {
    list = list.filter(p => p.category === selectedTab.value)
  }
  if (searchQuery.value) {
    list = list.filter(p => p.title.includes(searchQuery.value))
  }
  return list
})

// 제목 클릭
function openDetail(post) {
  currentPost.value = {
    ...post,
    image: 'https://via.placeholder.com/800x400.png?text=Your+Image',
    body:  '여기에 기사에 대한 설명이나 코멘트를 자유롭게 작성할 수 있습니다.'
  }
  showDetail.value = true
}
</script>

<style scoped>
.news-board {
  padding: 2rem 1rem;  /* padding을 줄여서 크기 일치 */
  background-color: #f0f6fd;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem; /* margin을 동일하게 설정 */
  /* width: 2120; */
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.tab {
  padding: 0.6rem 1rem;
  border: 1px solid #ccc;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.tab:hover {
  background-color: #f0f0f0;
}

.tab.active {
  background: #2f80ed;
  color: white;
  border-color: #2f80ed;
}

.search-bar {
  display: flex;
  justify-content: right;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.search-bar input {
  padding: 0.65rem 1rem;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1rem;
  width: 300px;
}

.search-bar input:focus {
  outline: none;
  border-color: #1e88e5;
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
}

.search-bar button {
  background-color: #455a64;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.search-bar button:hover {
  background-color: #263238;
}

.board-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
}

.board-table th, .board-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 1rem;
}

.board-table th {
  font-weight: 700;
  color: #333;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge {
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  font-size: 0.85rem;
  color: white;
}

.badge.review { background: #3b82f6; } /* 파랑 */
.badge.news   { background: #10b981; } /* 초록 */
.badge.free   { background: #6b7280; } /* 회색 */

.title-cell a {
  color: #333;
  text-decoration: none;
  font-weight: 600;
}

.title-cell a:hover {
  text-decoration: underline;
}
</style>
