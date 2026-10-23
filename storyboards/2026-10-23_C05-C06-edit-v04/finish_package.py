from pathlib import Path
import sys,json,hashlib,shutil,subprocess,re,struct,html
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
WIN=Path('C:/Users/wseok/.cache/codex-flow/Q-AI-Fair-C05-C06-edits-2026-10-23')
FF=OUT.parent/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vhash(p):
 h=hashlib.sha256()
 with av.open(str(p)) as con:
  for packet in con.demux(video=0):
   if packet.size:h.update(bytes(packet))
 return h.hexdigest()
def atom_order(p):
 boxes=[]
 with p.open('rb') as f:
  while True:
   buf=f.read(8)
   if len(buf)!=8:break
   size,kind=struct.unpack('>I4s',buf);header=8
   if size==1:size=struct.unpack('>Q',f.read(8))[0];header=16
   boxes.append(kind.decode('ascii'))
   if size==0:break
   f.seek(size-header,1)
 return boxes
titles={'C05':'괴수는 퇴근할 수 없다','C06':'퇴근 좀 해주세요'}
files=[];cards=[];checks={}
for c in titles:
 final=OUT/c/f'{c}_Q-AI_Fair_edit_v04.mp4'
 tv=json.loads((OUT/c/'technical_validation.json').read_text(encoding='utf-8'))
 assert sha(final)==tv['sha256']
 assert tv['max_audio_pts_gap_seconds']<1/48000
 assert tv['all_sfx_boundary_samples_zero']
 assert vhash(final)==vhash(OUT/c/f'{c}_picture.mp4')
 boxes=atom_order(final);assert boxes.index('moov')<boxes.index('mdat')
 proc=subprocess.run([str(FF),'-hide_banner','-i',str(final),'-vf','freezedetect=n=-50dB:d=0.5,blackdetect=d=0.08:pix_th=0.02','-an','-f','null','-'],capture_output=True,check=True)
 alerts=[s.strip() for s in proc.stderr.decode(errors='replace').splitlines() if 'freeze_' in s or 'black_start:' in s]
 checks[c]=dict(video_packets_unchanged_from_reviewed_render=True,video_packet_sha256=vhash(final),faststart=True,top_level_boxes=boxes,
    frozen_or_black_frame_detector_events=alerts,expected_static_ending_from=44 if c=='C06' else None,
    actual_player_playback=False,actual_listening=False)
 shutil.copy2(final,WIN/final.name);assert sha(WIN/final.name)==tv['sha256']
 files.append(dict(film=c,repo_path=str(final.relative_to(ROOT)),local_path=str(WIN/final.name),duration_seconds=tv['duration_seconds'],sha256=tv['sha256']))
 im=OUT/c/'review_frames'/('28.500s.png' if c=='C05' else '00.500s.png')
 shutil.copy2(im,WIN/f'{c}_v04_poster.png')
 cards.append(f'<section><h2>{int(c[1:])}번 · {titles[c]}</h2><p>{tv["duration_seconds"]:g}초 · v04 · 자막·효과음 타이밍 수정</p><video controls preload="metadata" poster="{c}_v04_poster.png" src="{final.name}"></video><p><a href="{final.name}" download>MP4 저장</a></p></section>')
 manifest=json.loads((OUT/c/'edit_manifest.json').read_text(encoding='utf-8'))
 manifest['status']='시각·효과음 배치 3인 재확인 및 기술 검증 완료. 실청취/실시간 플레이어 재생 미검증.'
 dump(OUT/c/'edit_manifest.json',manifest)
dump(OUT/'playback_file_checks.json',checks)
dump(OUT/'delivery_manifest.json',dict(files=files,viewer=str(WIN/'index.html')))
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q-AI Fair · 5번·6번 v04</title><style>body{margin:0;background:#0b121b;color:#f5f8fa;font:18px/1.65 "Malgun Gothic",sans-serif}main{max-width:1160px;margin:48px auto;padding:0 24px}h1{font-size:38px}p,small{color:#b5c7d1}section{margin:40px 0 64px}video{display:block;width:100%;border-radius:14px;background:#000}a{color:#8ce6d4}</style><main><h1>Q-AI Fair · 5번·6번 수정본</h1><p>효과음 위치·재질을 조정하고 대기 구간을 줄였습니다. 화면과 자막으로 내용을 전달합니다.</p>'''+''.join(cards)+'''<small>화면 표본·음원 수치·파일 검사는 완료했습니다. 도구를 통한 실제 청취·실시간 플레이어 재생 확인은 하지 못했습니다. 기존 편집본과 Flow 원본은 보존했습니다.</small></main></html>'''
(WIN/'index.html').write_text(page,encoding='utf-8')
(OUT/'README.md').write_text('''# 5번·6번 편집·효과음 수정 v04

- [5번 · 괴수는 퇴근할 수 없다 · 37.75초](C05/C05_Q-AI_Fair_edit_v04.mp4)
- [6번 · 퇴근 좀 해주세요 · 48.75초](C06/C06_Q-AI_Fair_edit_v04.mp4)

5번은 자막 종료 후 홀드 0.75초를 줄였습니다. 손을 지붕에서 떼는 원인은 보존했습니다. 기둥 착지·지붕 하중 효과음을 동작에 맞추고, 잭의 이중 클릭과 사다리의 종이 소리를 바퀴 마찰로 교체했습니다.

6번은 의자를 펴기 전 준비 0.75초와 반응 초반 0.5초를 줄였습니다. 문닫힘은 25.333초, 의자 펼침은 39.042초에 맞췄습니다. 펜에는 필기 마찰을 넣고, 불필요한 팻말 클릭은 삭제했습니다. 자막 읽기 시간과 엔딩 4.75초는 유지했습니다.

기존 음악의 선율·악기는 유지하며 편집에 맞춰 연결했습니다. 기존 효과음 믹스는 제외하고 재질별 낮은 강도의 새 효과음을 만들었습니다. 앞뒤 램프, 약한 합성 배경 기류, 고정 음량 게인과 끝 페이드를 적용했습니다. 음성 대사·추가 Flow·유료 API는 없습니다. 기존 영상과 원본은 그대로입니다.

검수자 3명이 실제 렌더 프레임·큐 기록을 독립 검토하고, 의견을 교차 확인한 뒤 수정본을 다시 확인했습니다. [검수 기록](review_summary.json), [파일 재생 관련 검사](playback_file_checks.json), [5번 기술 검사](C05/technical_validation.json), [6번 기술 검사](C06/technical_validation.json)를 보세요. 실제 값은 loudness의 input_i/input_tp입니다. output_*는 분석 도구의 가상 보정 결과이며 본 파일에 적용한 값이 아닙니다.

**실시간 플레이어 재생과 실제 청취는 확인하지 못했습니다.** Browser Use는 file: 페이지 관찰을 정책상 차단했고, 미디어 플레이어는 최초 개인정보 설정 단계라 변경하지 않았습니다. 우회하지 않고 파일 디코딩·프레임/AAC 시간축·무검정/정지 검사를 수행했습니다. 이 검사를 실청취·관객 반응 검증으로 확대하지 않습니다.

v04 중간 렌더에서 동적 음량 필터/리미터 조합의 55ms 오디오 시간 간격을 발견해 최종본에서 제거했습니다. 기존 전달본 v03에는 해당 간격이 없었습니다. 최종 오디오는 영상 끝까지 시간 간격 없이 이어지며, 최종 오디오 교체 전후 비디오 패킷은 동일합니다.

기존 5번의 처마 진입/사다리 브레이크 시간 생략과 작은 잔해 차이는 그대로입니다. [이전 v03 패키지](../2026-10-23_C05-C06-edit-v03/README.md)도 보존했습니다.
''',encoding='utf-8')
(ROOT/'00_완성_영상.md').write_text('''# Q-AI Fair · 5번·6번 최신 편집본 v04

화면과 후처리 자막으로 내용을 전달합니다. BGM·효과음은 보조이며 필수 대사는 없습니다.

| 작품 | 최신 MP4 | 길이 |
|---|---|---:|
| 5번 · 괴수는 퇴근할 수 없다 | [보기·다운로드](storyboards/2026-10-23_C05-C06-edit-v04/C05/C05_Q-AI_Fair_edit_v04.mp4) | 37.75초 |
| 6번 · 퇴근 좀 해주세요 | [보기·다운로드](storyboards/2026-10-23_C05-C06-edit-v04/C06/C06_Q-AI_Fair_edit_v04.mp4) | 48.75초 |

이번에는 문닫힘·의자 펼침·지붕 하중의 효과음 타이밍을 맞추고, 잭·사다리·펜의 소리를 동작에 맞게 바꿨습니다. 불필요한 클릭을 줄이고 짧은 페이드를 넣었습니다. 5번 대기 0.75초, 6번 준비·반응 1.25초를 줄였으며 자막과 엔딩 읽기 시간은 유지했습니다. 새 Flow 크레딧 사용은 **0**입니다.

두 파일 모두 1280×720, 24fps, H.264/AAC입니다. GitHub에서 재생이 안 되면 파일 페이지의 **Download raw file**을 누르세요.

3인 시각·효과음 배치 검수, 전체 디코딩, 프레임·오디오 시간축, 음량·피크 검사를 마쳤습니다. **실시간 플레이어 재생·실제 청취·행사장 테스트는 도구 제한으로 확인하지 못했습니다.** 청감 개선을 실청취로 확정한 결과는 아닙니다.

[수정·검수 상세](storyboards/2026-10-23_C05-C06-edit-v04/README.md) · [이전 편집본](storyboards/2026-10-23_C05-C06-edit-v03/README.md) · [Flow 원본·제작 이력](00_영상제작_현재상태.md) · [10안 콘티](README.md)
''',encoding='utf-8')
changes={
 'README.md':[('5번 38.5초 · 6번 50초. 후처리 자막·BGM·효과음 포함.','5번 37.75초 · 6번 48.75초. v04 효과음 타이밍·편집 호흡 수정.')],
 '00_영상제작_현재상태.md':[('38.5초·50초, 후처리 자막과 BGM·효과음 포함.','v04 37.75초·48.75초, 효과음 타이밍·편집 호흡 수정.')],
 '05_괴수는_퇴근할_수_없다.md':[('— 38.5초. 아래는','— v04 37.75초. 아래는')],
 '06_퇴근_좀_해주세요.md':[('— 50초. 아래는','— v04 48.75초. 아래는')]
}
for filename,replacements in changes.items():
 p=ROOT/filename;s=p.read_text(encoding='utf-8')
 for a,b in replacements:s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
p=ROOT/'RESUME_CODEX.txt';s=p.read_text(encoding='utf-8')
heading='[2026-10-23 C05·C06 재생/효과음 보정 v04]'
if not s.startswith(heading):
 p.write_text(heading+'''
최신요청: 재생과 효과음 어색함 수정. storyboards/2026-10-23_C05-C06-edit-v04/가 최신. C05 37.75초906프레임/C06 48.75초1170프레임,720p24fps. 자막·엔딩5/4.75초 유지. 기존원본과v03불변,Flow0/유료API0/예약재개0.
C05 홀드22.5~23.25(구시간) .75초삭제, 엄지손떼는원인유지. 기둥8초/지붕30.5초,잭·사다리바퀴음,이중click폐기. C06 의자준비37.75~38.5 및반응42.5~43(구시간)삭제;문25.333/의자39.042초,필기마찰/팻말click삭제. 원음무음유지·기존음악선율/악기유지·저강도새효과/짧은램프/배경기류/고정게인.
3인두편독립→교차→최종실제프레임/큐재확인. 새필수시각·배치문제0. v04중간동적음량필터의55msPTS간격발견해고정게인+연속PTS로해결(기존v03에는간격없었음). 최종전체디코딩/영상PTS/오디오말단·간격0/피크/비디오패킷불변검증. 검수자들은최종오디오교체후해시미확인,총괄이담당.
실청취·실시간플레이어재생은미검증:BrowserUse file:관찰정책차단우회안함,로컬미디어플레이어최초개인정보설정변경안하고닫음. 실제음색을들었다고말하지말것. 사용자최종승인아님. 최신2MP4/검수/SRT/재현코드Git반영,메인00_완성_영상.md. Windows기존갤러리최신v04링크/사본SHA동일. Push후remoteSHA확인하고보고.

'''+s,encoding='utf-8')
shutil.copy2(OUT.parent/'2026-10-23_C05-C06-edit-v03/GeneralUser-GS-LICENSE.txt',OUT/'GeneralUser-GS-LICENSE.txt')
print(json.dumps(dict(files=files,checks=checks),ensure_ascii=False,indent=2))
