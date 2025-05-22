<template>
  <div class="dashboard">
    <h1>금융 정보 통합 서비스</h1>
    <div class="card-grid">
      <RouterLink to="/map" class="card">은행 지도 보기</RouterLink>
      <RouterLink to="/compare" class="card">예금 금리 비교</RouterLink>
      <RouterLink to="/prices" class="card">현물 가격 변동 확인</RouterLink>
      <RouterLink to="/community" class="card">금융 커뮤니티</RouterLink>
      <RouterLink to="/recommend" class="card">금융 상품 추천</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  text-align: center;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.card {
  display: block;
  padding: 1.2rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  text-decoration: none;
  color: #333;
  font-weight: bold;
}
</style>
