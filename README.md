# KIHO Story Research — 무료 휴대폰용 PWA

## 특징
- 별도 OpenAI API 키와 서버 없이 작동하는 정적 웹앱입니다.
- 나무위키 문서의 본문을 복사해 넣고 ChatGPT Plus에 붙여넣을 분석 요청문을 만듭니다.
- ChatGPT 결과는 수동으로 붙여넣어 로컬 저장 및 텍스트 내보내기 가능합니다.
- 자동 웹 수집, 자동 사실 검증, ChatGPT 분석 결과의 자동 수신은 **지원하지 않습니다**.
- 별도 AI API 비용은 없지만 ChatGPT Plus 기존 구독료 및 사용량 제한은 그대로 적용됩니다.

## 무료 배포: GitHub Pages
1. GitHub 계정을 만들고 새 **Public** 저장소를 만듭니다.
2. 이 ZIP을 압축 해제하고 `index.html`, `app.js`, `sw.js`, `manifest.webmanifest`, `icons/`를 저장소 루트에 업로드합니다.
3. Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save.
4. 게시된 `https://계정.github.io/저장소명/` 주소를 휴대폰에서 엽니다. 배포 완료까지 시간이 걸릴 수 있습니다.
5. Android Chrome: 메뉴(⋮) → 홈 화면에 추가 또는 앱 설치. iPhone Safari: 공유 → 홈 화면에 추가.

GitHub Pages의 공개 저장소는 누구나 파일을 볼 수 있으므로 API 키나 비밀 자료를 저장소에 넣지 마세요. 이 앱의 입력 내용은 브라우저 로컬 저장소에만 저장되며, 사용자가 ChatGPT에 직접 붙여넣은 내용은 ChatGPT로 전송됩니다.

## 다른 무료 배포
Cloudflare Pages 또는 Netlify의 정적 사이트 무료 플랜을 이용할 수도 있습니다. 요금제와 제한은 배포 전 확인하세요.

## 테스트
로컬에서 `python3 -m http.server 8765` 실행 후 `http://localhost:8765` 접속. 모바일 PWA 설치에는 HTTPS 호스팅이 필요합니다.
