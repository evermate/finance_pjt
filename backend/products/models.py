'''
예금/적금은 한 모델로 통합하고,
연금은 구조가 달라서 별도 모델로 분리한다.
모든 금융상품은 Bank와 연동되며,
옵션/시뮬레이션은 하위 모델로 FK 연결된다.
'''
from django.db import models

# 금융회사 정보 (은행, 증권사 등)
class Bank(models.Model):
    fin_co_no = models.CharField(max_length=20, primary_key=True)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명

    def __str__(self):
        return self.kor_co_nm


# 예금 및 적금 상품 정보 (product_type으로 구분)
class DepositProduct(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ('deposit', '예금'),
        ('saving', '적금'),
    )

    fin_prdt_cd = models.CharField(max_length=50, primary_key=True)  # 금융상품 코드
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE) 
    fin_prdt_nm = models.CharField(max_length=100)  # 금융상품명
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)  # 예금/적금 구분
    join_way = models.TextField()  # 가입 방법
    mtrt_int = models.TextField() # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대 조건
    join_deny = models.CharField(max_length=1)  # 가입제한 Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.CharField(max_length=100)  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.BigIntegerField(null=True, blank=True)  # 최고 한도
    dcls_strt_day = models.CharField(max_length=8)  # 상품 공시 시작일
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True)  # 상품 공시 종료일
    fin_co_subm_day = models.CharField(max_length=14)  # 금융회사 제출일

    def __str__(self):
        return f"[{self.get_product_type_display()}] {self.fin_prdt_nm}"


# 예금/적금 상품의 금리 옵션 정보 (기간, 금리, 적금일 경우 적립 유형 포함)
class InterestOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    intr_rate_type = models.CharField(max_length=1)  # 저축 금리 유형 // S: 단리, M: 복리 등
    intr_rate_type_nm = models.CharField(max_length=20)  # 저축 금리 유형명
    save_trm = models.CharField(max_length=10)  # 저축 기간 // 단위: 개월

    # 적금 전용 필드 (정액/자유)
    rsrv_type = models.CharField(max_length=1, null=True, blank=True)  # 적립 유형 
    rsrv_type_nm = models.CharField(max_length=20, null=True, blank=True) # 적립 유형명

    intr_rate = models.FloatField(null=True, blank=True)   # 저축금리 // 소수점 2자리
    intr_rate2 = models.FloatField(null=True, blank=True)  # 최고우대금리 // 소수점 2자리

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.save_trm}개월 ({self.intr_rate_type_nm})"


# 연금저축 상품 정보 (펀드, 보험형 등)
# 현재 이 모델은 사용하지 않는다. 추후 연금저축 상품을 추가할 때 사용될 수 있다
class AnnuityProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=50, primary_key=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    fin_prdt_nm = models.CharField(max_length=200)
    join_way = models.TextField()
    pnsn_kind_nm = models.CharField(max_length=100)  # 연금 종류 (예: 연금저축펀드)
    prdt_type_nm = models.CharField(max_length=100)  # 상품 유형 (예: 주식형)
    avg_prft_rate = models.FloatField(null=True, blank=True)
    btrm_prft_rate_1 = models.FloatField(null=True, blank=True)
    btrm_prft_rate_2 = models.FloatField(null=True, blank=True)
    btrm_prft_rate_3 = models.FloatField(null=True, blank=True)
    mntn_cnt = models.BigIntegerField()
    sale_co = models.TextField()
    dcls_strt_day = models.CharField(max_length=8)
    fin_co_subm_day = models.CharField(max_length=14)

    def __str__(self):
        return self.fin_prdt_nm


# 연금저축 상품의 납입/수령 조건별 예상 수령액 시뮬레이션
# 현재 이 모델은 사용하지 않는다. 추후 연금저축 상품을 추가할 때 사용될 수 있다 
class AnnuitySimulation(models.Model):
    product = models.ForeignKey(AnnuityProduct, on_delete=models.CASCADE, related_name='simulations')
    pnsn_recp_trm_nm = models.CharField(max_length=50)   # 수령 기간
    pnsn_entr_age_nm = models.CharField(max_length=20)   # 가입 나이
    mon_paym_atm_nm = models.CharField(max_length=20)    # 월 납입액
    paym_prd_nm = models.CharField(max_length=20)        # 납입 기간
    pnsn_strt_age_nm = models.CharField(max_length=20)   # 연금 개시 나이
    pnsn_recp_amt = models.BigIntegerField()             # 예상 수령액

    def __str__(self):
        return f"{self.product.fin_prdt_nm} - {self.mon_paym_atm_nm} x {self.paym_prd_nm}"

