// <script setup>
// import { getBankIcon } from '@/utils/bankIconMap'

// const logoUrl = getBankIcon(bankName)
// </script>

// <template>
//   <img :src="getBankIcon(bankName)" alt="로고" class="bank-logo" />
// </template>


export function getBankIcon(bankName) {
  const map = {
    '우리은행': 'woori.png',
    '한국스탠다드차타드은행': 'scjeil.png',
    '아이엠뱅크': 'imbank.png',
    '부산은행': 'gyungnam_busan.png',
    '광주은행': 'gwangju_jungbook.png',
    '제주은행': 'shinhan_jeju.png',
    '전북은행': 'gwangju_jungbook.png',
    '경남은행': 'gyungnam_busan.png',
    '중소기업은행': 'ibk_giup.png',
    '한국산업은행': 'kdb_sanup.png',
    '국민은행': 'gookmin.png',
    '신한은행': 'shinhan_jeju.png',
    '농협은행주식회사': 'nonghyup.png',
    '하나은행': 'hana.png',
    '주식회사 케이뱅크': 'kbank.png',
    '수협은행': 'soohyup.png',
    '주식회사 카카오뱅크': 'kakao.png',
    '토스뱅크 주식회사': 'toss.png',
  }

  const filename = map[bankName] || 'default.png'
  return `/bank-icons/${filename}`
}

export function getBankLongIcon(bankName) {
  const map = {
    '우리은행': 'long_woori.png',
    '한국스탠다드차타드은행': 'long_scjeil.png',
    '아이엠뱅크': 'long_imbank.png',
    '부산은행': 'long_busanbank.png',
    '광주은행': 'long_gwangju.png',
    '제주은행': 'long_jeju.png',
    '전북은행': 'long_jungbook.png',
    '경남은행': 'long_gyungnam.png',
    '중소기업은행': 'long_ibk_giup.png',
    '한국산업은행': 'long_kdb_sanup.png',
    '국민은행': 'long_gookmin.png',
    '신한은행': 'long_shinhan.png',
    '농협은행주식회사': 'long_nonghyup.png',
    '하나은행': 'long_hana.png',
    '주식회사 케이뱅크': 'long_kbank.png',
    '수협은행': 'long_soohyup.png',
    '주식회사 카카오뱅크': 'long_kakao.png',
    '토스뱅크 주식회사': 'long_toss.png',
  }

  const filename = map[bankName] || 'default.png'
  return `/bank-icons-long/${filename}`
}
