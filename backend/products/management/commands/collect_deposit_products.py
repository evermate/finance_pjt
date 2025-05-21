import time
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from products.models import Bank, DepositProduct, InterestOption


class Command(BaseCommand):
    help = '금감원 예금 및 적금 상품을 수집하여 DB에 저장합니다.'

    def handle(self, *args, **kwargs):
        API_KEY = settings.FSS_API_KEY
        BASE_URL = 'http://finlife.fss.or.kr/finlifeapi'

        targets = [
            {'type': 'deposit', 'url': f'{BASE_URL}/depositProductsSearch.json'},
            {'type': 'saving',  'url': f'{BASE_URL}/savingProductsSearch.json'}
        ]

        for target in targets:
            self.stdout.write(self.style.NOTICE(f"📥 {target['type']} 수집 시작..."))
            page = 1
            max_page = None

            while True:
                params = {
                    'auth': API_KEY,
                    'topFinGrpNo': '020000',
                    'pageNo': page,
                }

                try:
                    res = requests.get(target['url'], params=params, timeout=10)
                    res.raise_for_status()
                    result = res.json().get('result', {})
                except (requests.RequestException, ValueError, KeyError) as e:
                    self.stderr.write(self.style.ERROR(f"❌ 요청 실패 (page {page}): {e}"))
                    break

                base_list = result.get('baseList', [])
                option_list = result.get('optionList', [])

                if page == 1:
                    max_page = result.get('max_page_no', 1)

                if not base_list:
                    self.stdout.write(self.style.WARNING(f"⚠️ 데이터 없음 (page {page})"))
                    break

                # 상품 저장
                for item in base_list:
                    bank, _ = Bank.objects.get_or_create(
                        fin_co_no=item['fin_co_no'],
                        defaults={'kor_co_nm': item['kor_co_nm']}
                    )

                    product, _ = DepositProduct.objects.update_or_create(
                        fin_prdt_cd=item['fin_prdt_cd'],
                        defaults={
                            'bank': bank,
                            'fin_prdt_nm': item['fin_prdt_nm'],
                            'product_type': target['type'],
                            'join_way': item['join_way'],
                            'mtrt_int': item['mtrt_int'],
                            'spcl_cnd': item['spcl_cnd'],
                            'join_deny': item['join_deny'],
                            'join_member': item['join_member'],
                            'etc_note': item['etc_note'],
                            'max_limit': item.get('max_limit') or None,
                            'dcls_strt_day': item['dcls_strt_day'],
                            'dcls_end_day': item.get('dcls_end_day'),
                            'fin_co_subm_day': item['fin_co_subm_day'],
                        }
                    )

                # 옵션 저장
                for option in option_list:
                    try:
                        product = DepositProduct.objects.get(fin_prdt_cd=option['fin_prdt_cd'])
                        InterestOption.objects.update_or_create(
                            product=product,
                            intr_rate_type=option['intr_rate_type'],
                            save_trm=option['save_trm'],
                            rsrv_type=option.get('rsrv_type'),
                            defaults={
                                'intr_rate_type_nm': option['intr_rate_type_nm'],
                                'intr_rate': option.get('intr_rate'),
                                'intr_rate2': option.get('intr_rate2'),
                                'rsrv_type_nm': option.get('rsrv_type_nm'),
                            }
                        )
                    except DepositProduct.DoesNotExist:
                        self.stderr.write(self.style.ERROR(f"❌ 옵션 저장 실패: 상품 코드 {option['fin_prdt_cd']} 없음"))

                if page >= max_page:
                    break

                page += 1
                time.sleep(0.3)  # 서버 보호용 지연

            self.stdout.write(self.style.SUCCESS(f"✅ {target['type']} 수집 완료"))

        self.stdout.write(self.style.SUCCESS('🎉 전체 수집 작업 완료'))
