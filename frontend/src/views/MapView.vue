<template>
  <!-- ✅ 상단 배너 추가 -->
    <div class="banner-section">
      <img src="/image/map.jpg" alt="시뮬레이션" class="banner-img" />
      <div class="banner-text">
        <h2>주변 은행 찾기</h2>
        <p>지역과 은행을 선택하고 가까운 지점을 확인해보세요</p>
      </div>
    </div>
  <div class="map-page">
    <!-- 좌측 필터 + 검색 결과 리스트 -->
    <div class="sidebar">
      <div class="filters">
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
        <button @click="searchBanks">🔍 검색</button>
        <button @click="enableManualMode" v-if="!manualMode">📍 현재 위치 수동 조정</button>
        <button @click="fixManualLocation" v-if="manualMode && manualLatLng">📌 위치 고정</button>
      </div>

      <div v-if="searchResults.length" class="results">
        <div class="result-item" v-for="(item, index) in searchResults" :key="index" @click="focusMarker(index)">
          <div class="bank-name">{{ item.place_name }}</div>
          <div class="bank-address">{{ item.address_name }}</div>
        </div>
      </div>
    </div>

    <!-- 지도 영역 -->
    <div class="map-area" ref="map"></div>
  </div>
</template>

<script setup>
// (기존 스크립트 유지, 단 searchResults 추가)
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { KAKAO_API_KEY, API_BASE_URL, KAKAO_MOBILITY_KEY } from '@/constants'
import data from '@/assets/data'

const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
const sidoOptions = data.mapInfo.map(r => r.name)
const sigunguOptions = ref([])
const bankOptions = data.bankInfo
const manualMode = ref(false)
const manualLatLng = ref(null)
const searchResults = ref([])

let kakaoMap = null
const map = ref(null)
let activeInfoWindow = null
let currentLocationMarker = null
let manualMarker = null
const markers = []
let activeMarker = null
let polyline = null // ✅ 길찾기 라인 저장용

const updateSigungu = () => {
  const region = data.mapInfo.find(r => r.name === selectedSido.value)
  sigunguOptions.value = region ? region.countries : []
  selectedSigungu.value = ''
}

const clearMarkers = () => {
  markers.forEach(marker => marker.setMap(null))
  markers.length = 0
  if (activeInfoWindow) activeInfoWindow.close()
  activeInfoWindow = null
  activeMarker = null
  if (polyline) polyline.setMap(null)
}

const searchBanks = () => {
  const query = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`
  axios.get(`${API_BASE_URL}/api/map/search-bank/`, { params: { query } })
    .then(res => {
      const data = res.data.documents
      searchResults.value = data
      clearMarkers()
      const bounds = new kakao.maps.LatLngBounds()
      data.forEach((place, idx) => {
        const position = new kakao.maps.LatLng(place.y, place.x)
        const marker = new kakao.maps.Marker({ map: kakaoMap, position })
        markers.push(marker)

        kakao.maps.event.addListener(marker, 'click', () => {
          if (activeInfoWindow) activeInfoWindow.close()
          if (activeMarker) activeMarker.setImage(null)

          const highlightedIcon = new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
            new kakao.maps.Size(24, 35)
          )
          marker.setImage(highlightedIcon)

          activeMarker = marker

          // ✅ 출발지 설정
          let origin = null
          if (manualLatLng.value) {
            origin = manualLatLng.value
            console.log('📍 수동 위치 사용:', origin.getLat(), origin.getLng())
          } else if (currentLocationMarker) {
            origin = currentLocationMarker.getPosition()
            console.log('📍 현재 위치 사용:', origin.getLat(), origin.getLng())
          } else {
            alert('출발 위치가 설정되지 않았습니다.')
            return
          }

          const destination = marker.getPosition()
          const originLng = origin.getLng()
          const originLat = origin.getLat()
          const destLng = destination.getLng()
          const destLat = destination.getLat()

          fetch(`https://apis-navi.kakaomobility.com/v1/directions?origin=${originLng},${originLat}&destination=${destLng},${destLat}&priority=RECOMMEND`, {
            method: 'GET',
            headers: {
              Authorization: KAKAO_MOBILITY_KEY
            }
          })
          .then(res => res.json())
          .then(data => {
            if (!data.routes?.length) {
              alert("경로 정보를 찾지 못했습니다.")
              return
            }

            const roads = data.routes[0].sections[0].roads
            const path = []
            roads.forEach(road => {
              for (let i = 0; i < road.vertexes.length; i += 2) {
                const lng = road.vertexes[i]
                const lat = road.vertexes[i + 1]
                path.push(new kakao.maps.LatLng(lat, lng))
              }
            })

            const distanceMeters = data.routes[0].summary.distance
            const distanceKm = (distanceMeters / 1000).toFixed(1)

            if (polyline) polyline.setMap(null)
            polyline = new kakao.maps.Polyline({
              map: kakaoMap,
              path: path,
              strokeWeight: 4,
              strokeColor: '#007aff',
              strokeOpacity: 0.9,
              strokeStyle: 'solid'
            })

            kakaoMap.setCenter(path[0])

            // ✅ 인포윈도우 업데이트
            const content = `
              <div style="position: relative; width: 300px; padding: 12px 16px; background: white; border: 2px solid #1976d2; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); font-family: Arial; font-size: 13px; line-height: 1.5; box-sizing: border-box;">
                <div style="font-weight: bold; font-size: 15px; color: #1976d2; margin-bottom: 8px;">${place.place_name}</div>
                <div><strong>주소:</strong> ${place.address_name}</div>
                <div><strong>도로명 주소:</strong> ${place.road_address_name || '-'}</div>
                <div><strong>거리:</strong> ${distanceKm}km</div>
                <button onclick="window.closeActiveInfoWindow()" style="position: absolute; top: 8px; right: 10px; background: none; border: none; font-size: 16px; font-weight: bold; color: #999; cursor: pointer;">&#10005;</button>
              </div>`

            const infowindow = new kakao.maps.InfoWindow({ content })
            infowindow.open(kakaoMap, marker)
            activeInfoWindow = infowindow
          })
          .catch(err => {
            console.error("경로 요청 실패", err)
            alert("경로 요청 중 오류가 발생했습니다.")
          })
        })

        bounds.extend(position)
      })
      kakaoMap.setBounds(bounds)
    })
    .catch(err => console.error('❌ 검색 실패:', err))
}

const focusMarker = (index) => {
  const marker = markers[index]
  const place = searchResults.value[index]
  if (!marker || !place) return
  if (activeInfoWindow) activeInfoWindow.close()
  if (activeMarker) activeMarker.setImage(null)

  const highlightedIcon = new kakao.maps.MarkerImage(
    'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
    new kakao.maps.Size(24, 35)
  )
  marker.setImage(highlightedIcon)

  const content = `
    <div style="position: relative; width: 300px; padding: 12px 16px; background: white; border: 2px solid #1976d2; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); font-family: Arial; font-size: 13px; line-height: 1.5; box-sizing: border-box;">
      <div style="font-weight: bold; font-size: 15px; color: #1976d2; margin-bottom: 8px;">${place.place_name}</div>
      <div><strong>주소:</strong> ${place.address_name}</div>
      <div><strong>도로명 주소:</strong> ${place.road_address_name || '-'}</div>
      
      <button onclick="window.closeActiveInfoWindow()" style="position: absolute; top: 8px; right: 10px; background: none; border: none; font-size: 16px; font-weight: bold; color: #999; cursor: pointer;">&#10005;</button>
    </div>`

  const infowindow = new kakao.maps.InfoWindow({ content })
  infowindow.open(kakaoMap, marker)
  kakaoMap.panTo(marker.getPosition())
  activeInfoWindow = infowindow
  activeMarker = marker
}

const enableManualMode = () => {
  manualMode.value = true
  manualLatLng.value = null
  if (currentLocationMarker) {
    currentLocationMarker.setMap(null)
    currentLocationMarker = null
  }
  kakao.maps.event.addListener(kakaoMap, 'click', handleMapClick)
}

const fixManualLocation = () => {
  manualMode.value = false
  kakao.maps.event.removeListener(kakaoMap, 'click', handleMapClick)
  if (!manualLatLng.value) return
  const redMarker = new kakao.maps.MarkerImage('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png', new kakao.maps.Size(24, 35))
  if (manualMarker) manualMarker.setMap(null)
  manualMarker = new kakao.maps.Marker({ map: kakaoMap, position: manualLatLng.value, image: redMarker })
  kakaoMap.setCenter(manualLatLng.value)
}

const handleMapClick = (mouseEvent) => {
  manualLatLng.value = mouseEvent.latLng

  if (manualMarker) manualMarker.setMap(null)
  if (polyline) polyline.setMap(null)

  const redMarker = new kakao.maps.MarkerImage('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png', new kakao.maps.Size(24, 35))
  manualMarker = new kakao.maps.Marker({
    map: kakaoMap,
    position: manualLatLng.value,
    image: redMarker,
    title: '선택한 위치'
  })

  kakaoMap.setCenter(manualLatLng.value)

  // ✅ 클릭과 동시에 고정되도록 처리
  manualMode.value = false
  kakao.maps.event.removeListener(kakaoMap, 'click', handleMapClick)
}

onMounted(() => {
  const script = document.createElement('script')
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&autoload=false`

  script.onload = () => {
    kakao.maps.load(() => {
      kakaoMap = new kakao.maps.Map(map.value, {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      })

      navigator.geolocation.getCurrentPosition(
        // ✅ 성공 콜백
        pos => {
          const userLoc = new kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude)
          console.log('✅ 현재 위치 가져오기 성공:', pos.coords)

          kakaoMap.setCenter(userLoc)

          const redMarker = new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            new kakao.maps.Size(24, 35)
          )

          currentLocationMarker = new kakao.maps.Marker({
            map: kakaoMap,
            position: userLoc,
            image: redMarker,
            title: '내 위치'
          })
        },

        // ❌ 실패 콜백
        err => {
          console.error('❌ 현재 위치 가져오기 실패:', err)

          const fallbackLoc = new kakao.maps.LatLng(37.5665, 126.9780)
          kakaoMap.setCenter(fallbackLoc)

          const redMarker = new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            new kakao.maps.Size(24, 35)
          )

          currentLocationMarker = new kakao.maps.Marker({
            map: kakaoMap,
            position: fallbackLoc,
            image: redMarker,
            title: '기본 위치 (서울 시청)'
          })

          alert('📍 현재 위치 정보를 사용할 수 없어 기본 위치로 설정했습니다.')
        }
      )
    })
  }

  document.head.appendChild(script)

  window.closeActiveInfoWindow = () => {
    if (activeInfoWindow) activeInfoWindow.close()
    activeInfoWindow = null
    if (activeMarker) activeMarker.setImage(null)
    activeMarker = null
  }
})


function initMap() {
  kakaoMap = new kakao.maps.Map(map.value, { center: new kakao.maps.LatLng(37.5665, 126.9780), level: 3 })
  navigator.geolocation.getCurrentPosition(pos => {
    const userLoc = new kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude)
    kakaoMap.setCenter(userLoc)
    const redMarker = new kakao.maps.MarkerImage('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png', new kakao.maps.Size(24, 35))
    currentLocationMarker = new kakao.maps.Marker({ map: kakaoMap, position: userLoc, image: redMarker, title: '내 위치' })
  }, err => console.error(err))
}
</script>

<style scoped>
.map-page {
  display: flex;
  gap: 1.5rem;
  padding: 2rem;
  background-color: #f5f8fb;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.title-card {
  max-width: 600px;
  margin: 1rem auto 2rem;
  padding: 1.5rem 2rem;
  border-radius: 16px;
  background: linear-gradient(to right, #e3ecf7, #f9fcff);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.title-card h1 {
  color: #2c3e50;
}

.title-card p {
  color: #6c7a92;
}

.sidebar {
  width: 360px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 1rem;
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.filters select,
.filters button {
  padding: 0.6rem 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  font-weight: 600;
}

.filters button {
  background: linear-gradient(to right, #a1c4fd, #c2e9fb);
  color: #2c3e50;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(161, 196, 253, 0.25);
}

.filters button:hover {
  background: linear-gradient(to right, #89bffa, #addcfb);
}

.results {
  border-top: 1px solid #ddd;
  margin-top: 1rem;
}

.result-item {
  padding: 0.85rem 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.result-item:hover {
  background-color: #f0f4f9;
}

.bank-name {
  font-weight: bold;
  color: #1a237e;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.bank-address {
  font-size: 0.88rem;
  color: #555;
}

.map-area {
  flex: 1;
  height: 90vh;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

@media screen and (max-width: 1024px) {
  .map-page {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    max-height: unset;
    position: static;
  }

  .map-area {
    height: 500px;
  }
}
.banner-section {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.banner-img {
  width: 100%;
  height: 250%;
  object-fit: cover;
  filter: brightness(0.6);
}

.banner-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 2;
}

.banner-text h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.banner-text p {
  font-size: 1.1rem;
  font-weight: 400;
}
</style>
