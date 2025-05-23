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
      <!-- ⬇️ controls div 내부 아래쪽에 추가 -->
      <div class="manual-controls">
        <button @click="enableManualMode" v-if="!manualMode">현재 위치 수동 조정</button>
        <button @click="fixManualLocation" v-if="manualMode && manualLatLng">위치 고정</button>
      </div>

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
let activeInfoWindow = null
let currentLocationMarker = null
let manualMarker = null

const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
const sidoOptions = data.mapInfo.map(r => r.name)
const sigunguOptions = ref([])
const bankOptions = data.bankInfo

const manualMode = ref(false)
const manualLatLng = ref(null)

const updateSigungu = () => {
  const region = data.mapInfo.find(r => r.name === selectedSido.value)
  sigunguOptions.value = region ? region.countries : []
  selectedSigungu.value = ''
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

const handleMapClick = (mouseEvent) => {
  const latlng = mouseEvent.latLng
  manualLatLng.value = latlng

  if (manualMarker) {
    manualMarker.setMap(null)
  }

  manualMarker = new kakao.maps.Marker({
    map: kakaoMap,
    position: latlng,
    title: '선택한 위치'
  })
}

const fixManualLocation = () => {
  manualMode.value = false
  kakao.maps.event.removeListener(kakaoMap, 'click', handleMapClick)

  const latlng = manualLatLng.value
  if (!latlng) return

  // ✅ 마커 이미지는 여기서 생성해야 안전
  const redMarkerImageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png'
  const imageSize = new kakao.maps.Size(24, 35)
  const redMarkerImage = new kakao.maps.MarkerImage(redMarkerImageSrc, imageSize)

  if (manualMarker) {
    manualMarker.setMap(null)
    manualMarker = new kakao.maps.Marker({
      map: kakaoMap,
      position: latlng,
      image: redMarkerImage,
      title: '고정 위치'
    })
  }

  kakaoMap.setCenter(latlng)
}

const markers = []

const clearMarkers = () => {
  markers.forEach(marker => marker.setMap(null))
  markers.length = 0

  if (activeInfoWindow) {
    activeInfoWindow.close()
    activeInfoWindow = null
  }
}

const searchBanks = () => {
  const query = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`
  axios.get(`${API_BASE_URL}/api/map/search-bank/`, { params: { query } })
    .then(res => {
      const data = res.data.documents
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
          if (activeInfoWindow) activeInfoWindow.close()
          infowindow.open(kakaoMap, marker)
          activeInfoWindow = infowindow
        })

        bounds.extend(position)
      })

      kakaoMap.setBounds(bounds)
    })
    .catch(err => console.error('❌ 검색 실패:', err))
}

onMounted(() => {
  const script = document.createElement('script')
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&autoload=false`
  script.onload = () => {
    kakao.maps.load(() => {
      initMap()
    })
  }
  document.head.appendChild(script)
})

function initMap() {
  kakaoMap = new kakao.maps.Map(map.value, {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 3
  })
  mapReady.value = true

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const lat = pos.coords.latitude
      const lng = pos.coords.longitude
      const userLocation = new kakao.maps.LatLng(lat, lng)
      kakaoMap.setCenter(userLocation)

      const redMarkerImageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png'
      const imageSize = new kakao.maps.Size(24, 35)
      const redMarkerImage = new kakao.maps.MarkerImage(redMarkerImageSrc, imageSize)

      currentLocationMarker = new kakao.maps.Marker({
        map: kakaoMap,
        position: userLocation,
        title: '내 위치',
        image: redMarkerImage
      })
    },
    (err) => {
      console.error('❌ 위치 권한 거부됨', err)
    }
  )
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
