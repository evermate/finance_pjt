from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Generate + Load demo fixture data in one step"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("📦 더미 데이터 생성 중 (generate_fixtures)..."))
        call_command('generate_fixtures')

        self.stdout.write(self.style.NOTICE("📥 더미 데이터 불러오는 중 (load_fixtures)..."))
        call_command('load_fixtures')

        self.stdout.write(self.style.SUCCESS("✅ 모든 더미 데이터 생성 및 로딩 완료"))
