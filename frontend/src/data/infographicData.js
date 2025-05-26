//// src/data/infographicData.js
// export default [
//   {
//     title: '2025년 평균 저축률',
//     description: '한국인의 평균 저축률',
//     chartType: 'doughnut',    // pie, doughnut, bar, line, horizontalBar, number 등
//     labels: ['저축률'],
//     data: [12.4],
//     unit: '%'
//   },
//   {
//     title: '연령대별 투자 비중',
//     description: '세대별 금융 상품 투자 분포',
//     chartType: 'bar',         // 수평 막대를 쓰려면 Chart.js 옵션 변경
//     labels: ['20대','30대','40대','50대 이상'],
//     data: [15,25,30,30],
//     unit: '%'
//   },
//   {
//     title: '부채 비율 추이',
//     description: 'GDP 대비 가계부채 비율 변화',
//     chartType: 'line',
//     labels: ['2015','2020','2025'],
//     data: [42,48,52],
//     unit: '%'
//   },
//   {
//     title: '주식 vs 예적금 선호도',
//     description: '투자 유형별 선호도 비교',
//     chartType: 'doughnut',
//     labels: ['주식','예·적금'],
//     data: [60,40],
//     unit: '%'
//   },
//   {
//     title: '가계 평균 자산 규모',
//     description: '2024년 기준 평균 순자산',
//     chartType: 'number',
//     value: '1.2억',
//     unit: '원'
//   },
//   {
//     title: '금융 앱 사용률',
//     description: '모바일 금융 서비스 활용도',
//     chartType: 'pie',
//     labels: ['사용자','비사용자'],
//     data: [70,30],
//     unit: '%'
//   },
// ]

// src/stores/infographicData.js

export const infographicItems = [
  {
    id: 1,
    title: '2025년 평균 저축률',
    value: 12.4,
    chartType: 'pie',
    labels: ['저축률', '미저축률'],
    data: [12.4, 100 - 12.4],
    description: '한국인의 평균 저축률'
  },
  {
    id: 2,
    title: '연령대별 투자 비중',
    chartType: 'bar',
    labels: ['20대', '30대', '40대', '50대 이상'],
    data: [15, 25, 30, 30],
    description: '세대별 금융 상품 투자 분포'
  },
  {
    id: 3,
    title: '부채 비율 추이',
    chartType: 'line',
    labels: ['2015', '2025'],
    data: [42, 52],
    description: 'GDP 대비 가계부채 비율 변화'
  },
  {
    id: 4,
    title: '주식 vs 예·적금 선호도',
    chartType: 'doughnut',
    labels: ['주식', '예·적금'],
    data: [60, 40],
    description: '투자 유형별 선호도 비교'
  },
  {
    id: 5,
    title: '가계 평균 자산 규모',
    value: 120_000_000,  // 1.2억원
    chartType: 'text',
    labels: [],
    data: [],
    description: '2024년 기준 평균 순자산'
  },
  {
    id: 6,
    title: '금융 앱 사용률',
    chartType: 'pie',
    labels: ['사용', '미사용'],
    data: [70, 30],
    description: '모바일 금융 서비스 활용도'
  }
]
