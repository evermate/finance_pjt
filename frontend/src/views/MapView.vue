<template>
  <h1 style="text-align: center;">🏦 주변 은행 찾기</h1>
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
import { KAKAO_API_KEY, API_BASE_URL } from '@/constants'
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

        const content = `
          <div style="position: relative; width: 300px; padding: 12px 16px; background: white; border: 2px solid #1976d2; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); font-family: Arial; font-size: 13px; line-height: 1.5; box-sizing: border-box;">
            <div style="font-weight: bold; font-size: 15px; color: #1976d2; margin-bottom: 8px;">${place.place_name}</div>
            <div><strong>주소:</strong> ${place.address_name}</div>
            <div><strong>도로명 주소:</strong> ${place.road_address_name || '-'}</div>
            
            <button onclick="window.closeActiveInfoWindow()" style="position: absolute; top: 8px; right: 10px; background: none; border: none; font-size: 16px; font-weight: bold; color: #999; cursor: pointer;">&#10005;</button>
          </div>`

        const infowindow = new kakao.maps.InfoWindow({ content })

        kakao.maps.event.addListener(marker, 'click', () => {
          if (activeInfoWindow) activeInfoWindow.close()
          if (activeMarker) activeMarker.setImage(null)

          const highlightedIcon = new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
            new kakao.maps.Size(24, 35)
          )
          marker.setImage(highlightedIcon)

          infowindow.open(kakaoMap, marker)
          activeInfoWindow = infowindow
          activeMarker = marker
        })

        bounds.extend(position)
      })
      kakaoMap.setBounds(bounds)
    })
    .catch(err => console.error('\u274c \uac80색 \uc2e4패:', err))
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
  manualMarker = new kakao.maps.Marker({ map: kakaoMap, position: manualLatLng.value, title: '선택한 위치' })
}

onMounted(() => {
  const script = document.createElement('script')
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&autoload=false`
  script.onload = () => {
    kakao.maps.load(() => {
      kakaoMap = new kakao.maps.Map(map.value, { center: new kakao.maps.LatLng(37.5665, 126.9780), level: 3 })
      navigator.geolocation.getCurrentPosition(pos => {
        const userLoc = new kakao.maps.LatLng(pos.coords.latitude, pos.coords.longitude)
        kakaoMap.setCenter(userLoc)
        const redMarker = new kakao.maps.MarkerImage('https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png', new kakao.maps.Size(24, 35))
        currentLocationMarker = new kakao.maps.Marker({ map: kakaoMap, position: userLoc, image: redMarker, title: '내 위치' })
      }, err => console.error(err))
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
  padding: 1.5rem;
}
.sidebar {
  width: 360px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  padding: 1rem;
  max-height: 80vh;
  overflow-y: auto;
}
.filters {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.filters select, .filters button {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.results {
  border-top: 1px solid #eee;
  margin-top: 1rem;
}
.result-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}
.result-item:hover {
  background-color: #f9f9f9;
}
.bank-name {
  font-weight: bold;
  color: #1a237e;
}
.bank-address {
  font-size: 0.9rem;
  color: #555;
}
.map-area {
  flex: 1;
  height: 80vh;
  border-radius: 12px;
  overflow: hidden;
}
.title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
</style>
