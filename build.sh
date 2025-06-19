#!/usr/bin/env bash

# 시스템 패키지 업데이트 및 한글 폰트 설치
apt-get update && apt-get install -y fonts-noto-cjk

# matplotlib 설정 폴더 생성
mkdir -p ~/.config/matplotlib

# matplotlib 설정 파일에 폰트 지정
echo "font.family: 'Noto Sans CJK KR'" > ~/.config/matplotlib/matplotlibrc
