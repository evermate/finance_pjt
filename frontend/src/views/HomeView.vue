<!-- src/views/HomeView.vue -->
<template>
  <div class="hero-section">
    <div class="container">
      <h1>Elevate Your Financial Management</h1>
      <h2>Bank</h2>
      <!-- <RouterLink to="/compare" class="cta">지금 금리 비교 시작</RouterLink> -->
    </div>
  </div>

  <div class="cards-wrapper">
    <div class="container cards">
      <RouterLink to="/compare" class="card">
        <img src="/image/weighing-scale.png" alt="예적금 금리 비교" />
        <p>예적금 금리 비교</p>
      </RouterLink>

      <RouterLink to="/recommend" class="card">
        <img src="/image/search.png" alt="금융 상품 추천" />
        <p>금융 상품 추천받기</p>
      </RouterLink>

      <RouterLink to="/map" class="card">
        <img src="/image/compass.png" alt="은행 검색" />
        <p>주변 은행 검색</p>
      </RouterLink>
      <!-- 여기 자산 시뮬레이션 카드 추가 -->
      <RouterLink to="/simulation" class="card">
         <img src="/image/wealth_simulation.png" alt="자산 시뮬레이션" />
        <p>은퇴 자산 시뮬레이션</p>
      </RouterLink>
    </div>
  </div>

  <ProductSlider :limit="2" title="주목할만한 금융상품" />
  <!-- ── 여기에 인포그래픽 섹션 추가 ── -->
   <NewsBoard />
  <!-- <InfographicSection /> -->

  <footer class="footer">
    <div class="container footer-grid">
      <div class="footer-left">
        <img src="/image/MainLogo.png" alt="Logo" class="footer-logo" />
        <div class="sns-icons">
          <img src="/image/Icon.png" alt="icon" />
          <img src="/image/Logo Instagram.png" alt="instagram" />
          <img src="/image/Logo YouTube.png" alt="youtube" />
          <img src="/image/LinkedIn.png" alt="linkedin" />
        </div>
      </div>
      <div>
        <p class="footer-title">서비스</p>
        <ul>
          <li>공지사항</li>
          <li>자주 묻는 질문</li>
          <li>계정 일시잠금</li>
          <li>고객센터</li>
          <li>개인정보 이용 내역</li>
        </ul>
      </div>
      <div>
        <p class="footer-title">문의</p>
        <ul>
          <li>사업 제휴</li>
          <li>광고 문의</li>
          <li>인증 사업 문의</li>
          <li>마케팅 / PR</li>
          <li>IR</li>
        </ul>
      </div>
      <div>
        <p class="footer-title">고객센터</p>
        <ul>
          <li>전화: 1588-1111</li>
          <li>이메일(고객전용): support@bank</li>
          <li>이메일(외부기관전용): middle@bank</li>
          <li>민원 접수</li>
          <li>민원 접수(비즈니스 고객)</li>
        </ul>
      </div>
    </div>
  </footer>
</template>


<script setup>
// 기존 임포트들...
import ProductSlider from '@/components/ProductSlider.vue'
import NewsBoard         from '@/components/Eda/NewsBoard.vue'
import InfographicSection from '@/components/Eda/InfographicSection.vue'
</script>

<style scoped>
.hero-section {
  background: linear-gradient(to right, #2f80ed, #56ccf2);
  color: white;
  text-align: center;
  padding: 4rem 1rem 6rem;
  position: relative;
  z-index: 1;
}

.hero-section .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
}

.hero-section h1 {
  font-size: 2.4rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.hero-section h2 {
  font-size: 1.6rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.cta {
  display: inline-block;
  background-color: white;
  color: #2f80ed;
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 0;
  text-decoration: none;
}

.cards-wrapper {
  margin-top: -80px;
  padding: 0 1rem 5rem;
  background-color: transparent;
  position: relative;
  z-index: 2;
}

.cards {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
  height: 200px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
    justify-content: center;  /* 세로 중앙 정렬 */
  align-items: center;      /* 가로 중앙 정렬 */
  gap: 0.75rem;             /* 이미지와 텍스트 사이 간격 */
}

.card {
  background-color: white;
  color: black;
  border-radius: 12px;
  width: 180px;
  padding: 1.2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  text-align: center;
  text-decoration: none;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card img {
  width: 60px;
  height: 60px;
  margin-bottom: 0.5rem;
  /* object-fit: contain; */
}

.card p {
  font-weight: bold;
  font-size: 1rem;
  margin: 0;
}

.footer {
  background-color: #e0dede;
  padding: 3rem 2rem;
  color: #333;
  font-size: 0.875rem;
}

.footer-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: flex-start;
  gap: 2.5rem;
  flex-direction: row;
  text-align: left;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.footer-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
  min-width: 160px;
}

.footer-logo {
  height: 30px;
}

.sns-icons {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.sns-icons img {
  width: 24px;
  height: 24px;
}

.footer-title {
  font-weight: bold;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.footer-grid ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-grid li {
  margin-bottom: 0.3rem;
}

@media screen and (max-width: 768px) {
  .cards {
    flex-direction: column;
    align-items: center;
  }
  .footer-grid {
    flex-direction: column;
    align-items: center;
    gap: 2rem;
  }
  .footer-left {
    align-items: center;
  }
}
</style>
