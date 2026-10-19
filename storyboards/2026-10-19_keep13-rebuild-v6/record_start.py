from pathlib import Path
R=Path(__file__).resolve().parent
root=R.parent.parent
p=root/'RESUME_CODEX.txt'
old=p.read_bytes()
notice='''[2026-10-19 V6 진행 중 — 최신 사용자 지시]
V5의 C01 「성공 자세 교정원」과 C03 「환경까지 가져왔습니다」 유지. C02/C04/C05는 재미·돌고래유괴단 감성 부족으로 재작성, 등장인물의 나이·체형·헤어·얼굴 실루엣 다양화 요청.
새 작업: storyboards/2026-10-19_keep13-rebuild-v6/
기존 두 콘티 객체와 채택 PNG 17장 복사·SHA 대조 완료. 기존 완성 C01 36초 v07 영상도 SHA 일치.
현재 단계: 자료 재분석 및 두 작가 독립 발상. 새 이미지 제작 전 기획 재검토 예정. 아직 완료본 아님.
Flow·동영상·음원 생성 금지. ai-flow 예약 PAUSED 확인. 이전 V5는 제작 기록으로 보존하되 이번 사용자가 선택한 것은 C01/C03만이다.

'''
if not old.startswith(notice.encode('utf-8')):p.write_bytes(notice.encode('utf-8')+old)
print('Latest scope saved; prior handoff bytes preserved.')
