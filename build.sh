#!/bin/bash

# 시스템 패키지 업데이트
apt-get update

# 한글 폰트 설치 (Noto Sans CJK 포함)
apt-get install -y fonts-noto-cjk

# 필요한 Python 패키지 설치
pip install -r requirements.txt

# Flask 서버 실행은 render.yaml에서 함
