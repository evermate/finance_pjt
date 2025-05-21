import time
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from products.models import Bank, AnnuityProduct, AnnuitySimulation


class Command(BaseCommand):
    help = '금감원 연금저축 상품 전체 페이지 수집 (디버깅 로그 포함)'

    def handle(self, *args, **kwargs):
        API_KEY = settings.FSS_API_KEY
        BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/annuitySavingProductsSearch.json'
        page = 1
        max_page = None

        self.stdout.write(self.style.NOTICE("📥 연금저축 상품 전체 수집 시작..."))

        while True:
            print(f"\n📡 요청 중... page {page}")
            params = {
                'auth': API_KEY,
                'topFinGrpNo': '060000',
                'pageNo': page,
            }

            try:
                res = requests.get(BASE_URL, params=params, timeout=10)
                res.raise_for_status()
                result = res.json().get('result', {})
            except (requests.RequestException, ValueError, KeyError) as e:
                self.stderr.write(self.style.ERROR(f"❌ 요청 실패 (page {page}): {e}"))
                break

            base_list = result.get('baseList', [])
            option_list = result.get('optionList', [])

            if page == 1:
                max_page = result.get('max_page_no')
                if not max_page:
                    self.stderr.write(self.style.ERROR("❌ max_page_no를 받아오지 못했습니다."))
                    break
                print(f"🔎 전체 페이지 수: {max_page}")

            print(f"📦 상품 {len(base_list)}개 / 시뮬레이션 {len(option_list)}개 수신됨")

            if not base_list:
                self.stdout.write(self.style.WARNING(f"⚠️ baseList 비어있음 (page {page})"))
                break

            for item in base_list:
                bank, _ = Bank.objects.get_or_create(
                    fin_co_no=item['fin_co_no'],
                    defaults={'kor_co_nm': item['kor_co_nm']}
                )

                product, _ = AnnuityProduct.objects.update_or_create(
                    fin_prdt_cd=item['fin_prdt_cd'],
                    defaults={
                        'bank': bank,
                        'fin_prdt_nm': item['fin_prdt_nm'],
                        'join_way': item['join_way'],
                        'pnsn_kind_nm': item['pnsn_kind_nm'],
                        'prdt_type_nm': item['prdt_type_nm'],
                        'avg_prft_rate': item.get('avg_prft_rate'),
                        'btrm_prft_rate_1': item.get('btrm_prft_rate_1'),
                        'btrm_prft_rate_2': item.get('btrm_prft_rate_2'),
                        'btrm_prft_rate_3': item.get('btrm_prft_rate_3'),
                        'mntn_cnt': item.get('mntn_cnt') or 0,
                        'sale_co': item.get('sale_co') or '',
                        'dcls_strt_day': item['dcls_strt_day'],
                        'fin_co_subm_day': item['fin_co_subm_day'],
                    }
                )

            for sim in option_list:
                try:
                    product = AnnuityProduct.objects.get(fin_prdt_cd=sim['fin_prdt_cd'])
                    AnnuitySimulation.objects.update_or_create(
                        product=product,
                        pnsn_recp_trm_nm=sim['pnsn_recp_trm_nm'],
                        pnsn_entr_age_nm=sim['pnsn_entr_age_nm'],
                        mon_paym_atm_nm=sim['mon_paym_atm_nm'],
                        paym_prd_nm=sim['paym_prd_nm'],
                        pnsn_strt_age_nm=sim['pnsn_strt_age_nm'],
                        defaults={
                            'pnsn_recp_amt': sim['pnsn_recp_amt'],
                        }
                    )
                except AnnuityProduct.DoesNotExist:
                    self.stderr.write(self.style.ERROR(f"❌ 시뮬레이션 저장 실패: 상품 코드 {sim['fin_prdt_cd']} 없음"))

            # ✅ 디버깅용 출력
            print(f"✅ page {page} 저장 완료\n---")

            if page >= max_page:
                break

            page += 1
            time.sleep(0.3)  # 호출 간 짧은 대기

        self.stdout.write(self.style.SUCCESS("🎉 연금저축 상품 전체 수집 완료"))
