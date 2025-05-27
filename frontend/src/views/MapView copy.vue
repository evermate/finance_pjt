<template>
  <div class="map-container">
    <h1>지역 검색 테스트</h1>

    <div class="controls">
      <select v-model="selectedSido" @change="updateSigungu">
        <option disabled value="">광역시/도 선택</option>
        <option v-for="sido in sidoOptions" :key="sido">{{ sido }}</option>
      </select>

      <select v-model="selectedSigungu">
        <option disabled value="">시/군/구 선택</option>
        <option v-for="gu in sigunguOptions" :key="gu">{{ gu }}</option>
      </select>

      <select v-model="selectedBank">
        <option disabled value="">은행명 선택</option>
        <option v-for="bank in bankOptions" :key="bank">{{ bank }}</option>
      </select>

      <button @click="searchBanks">검색</button>
    </div>

    <div ref="map" class="map"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { KAKAO_API_KEY, API_BASE_URL } from '@/constants'
import data from '@/assets/data'

const map = ref(null)
const mapReady = ref(false)
let kakaoMap = null
let activeInfoWindow = null  // 현재 열려 있는 InfoWindow를 기억


const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
const sidoOptions = data.mapInfo.map(r => r.name)
const sigunguOptions = ref([])
const bankOptions = data.bankInfo

const updateSigungu = () => {
  const region = data.mapInfo.find(r => r.name === selectedSido.value)
  sigunguOptions.value = region ? region.countries : []
  selectedSigungu.value = ''
}

// const logQuery = () => {
//   const query = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`
//   console.log('🔍 검색 쿼리:', query)
// }

onMounted(() => {
  const script = document.createElement('script')
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&autoload=false`
  script.onload = () => {
    kakao.maps.load(() => {
      kakaoMap = new kakao.maps.Map(map.value, {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      })
      mapReady.value = true
      // console.log('✅ 지도 로딩 완료')

      // ✅ 여기서 위치 가져오기 실행!
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const lat = pos.coords.latitude
          const lng = pos.coords.longitude
          // console.log('📍 내 위치:', lat, lng)

          const userLocation = new kakao.maps.LatLng(lat, lng)

          // 지도 중심 이동
          kakaoMap.setCenter(userLocation)

          // 마커 생성
          new kakao.maps.Marker({
            map: kakaoMap,
            position: userLocation,
            title: '내 위치'
          })
        },
        (err) => {
          console.error('❌ 위치 권한 거부됨', err)
        }
      )
    })
  }
  document.head.appendChild(script)
})


const markers = []

const clearMarkers = () => {
  markers.forEach(marker => marker.setMap(null))
  markers.length = 0

  // ✅ 열린 인포윈도우도 닫아주기
  if (activeInfoWindow) {
    activeInfoWindow.close()
    activeInfoWindow = null
  }
}

const searchBanks = () => {
  const query = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`
  // console.log('🔍 검색 쿼리:', query)

  axios.get(`${API_BASE_URL}/api/map/search-bank/`, { params: { query } })
    .then(res => {
      const data = res.data.documents
      // console.log('✅ 검색 결과:', data)

      clearMarkers()

      const bounds = new kakao.maps.LatLngBounds()

      data.forEach(place => {
        const position = new kakao.maps.LatLng(place.y, place.x)

        const marker = new kakao.maps.Marker({
          map: kakaoMap,
          position
        })

        markers.push(marker)

        const infowindow = new kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:14px;">${place.place_name}</div>`
        })

        kakao.maps.event.addListener(marker, 'click', () => {
          if (activeInfoWindow) {
            activeInfoWindow.close()  // 이전 InfoWindow 닫기
          }
          infowindow.open(kakaoMap, marker)
          activeInfoWindow = infowindow  // 새로 연 InfoWindow 기억
        })

        bounds.extend(position)
      })

      kakaoMap.setBounds(bounds)
    })
    .catch(err => {
      console.error('❌ 검색 실패:', err)
    })
}


</script>

<style scoped>
.map-container {
  padding: 16px;
}

.controls {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

select,
button {
  padding: 8px;
}

.map {
  width: 100%;
  height: 500px;
  border: 1px solid #ccc;
}
</style>
