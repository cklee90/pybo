from .base import * # base 에 있는 모든내용 사용하고 ALLOWED_HOSTS 만 따로씀


ALLOWED_HOSTS = ["13.124.46.151"] #AWS 고정 IP
STATIC_ROOT = BASE_DIR / 'static/'

#이유는 STATIC_ROOT가 설정된 경우 STATICFILES_DIRS 리스트에 STATIC_ROOT와 동일한 디렉터리가 포함되어 있으면
# 서버 실행 시 다음과 같은 오류가 발생
STATICFILES_DIRS = []