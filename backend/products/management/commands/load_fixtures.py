from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = "Load all fixture JSON files from the fixtures directory in correct order"

    def handle(self, *args, **kwargs):
        FIXTURE_DIR = "fixtures"
        fixture_files = [
            "users_fixture.json",
            "posts_fixture.json",
            "comments_fixture.json",
            "joined_products_fixture.json",
            "post_likes_fixture.json",
        ]

        for file in fixture_files:
            full_path = os.path.join(FIXTURE_DIR, file)
            if not os.path.exists(full_path):
                self.stdout.write(self.style.WARNING(f"⚠️  {full_path} 파일이 존재하지 않음. 스킵합니다."))
                continue

            self.stdout.write(self.style.NOTICE(f"📦 {file} 로드 중..."))
            try:
                call_command('loaddata', full_path)
                self.stdout.write(self.style.SUCCESS(f"✅ {file} 로드 완료"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ {file} 로드 실패: {e}"))
