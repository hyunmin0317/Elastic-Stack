# 키바나 node-js 버전 확인
cat package.json

# nvm 설치
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# 홈 디렉토리에서 .bashrc 실행
source .bashrc

# node-js 설치
nvm install 16.13.0

# pm2 설치
npm install pm2 -g