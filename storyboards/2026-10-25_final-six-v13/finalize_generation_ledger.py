from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
g=json.loads((P/'generation_log.json').read_text(encoding='utf-8-sig'))
accepted={
'C01_K06_pose_bridge':([.5,4],'코치가 누운 상태에서 팔·다리를 올림. 새 근접 눕기/모방 컷과 연결.'),
'C04_K01_note_push':([.5,5.5],'쪽지가 손에서 완전히 분리되어 틈 안으로 들어가고 빈 손이 빠짐.'),
'C02_K05_shortchain':([.5,5],'take02만 채택: 두 수갑과 짧은 사슬, 손 분리.'),
'C04_K08_hinges':([1,4],'세 경첩 창문 열림, 정확히 세 인물.'),
'C01_K07_close_recline':([1,4.25],'수강자 근접 화면에서 등과 머리를 매트로 내림.'),
'C01_K08_mirror':([1,5.5],'서로 다른 매트에서 같은 팔·다리 포즈. 코치의 작은 각도 조절 수용.')}
holds={
'C01_K07_lower_back':'코치 소실. 채택 금지.',
'C02_K05_shortchain':'take01: 고리가 세 개. take02로 대체.',
'C05_N05_hand_transfer':'한손 이동은 보이나 1.5/2.5/3.5초 단목 포식자형 얼굴이 드러나 원래 긴 목 인형과 불일치. 전부 제외.',
'C05_N06_pivot':'단목 근육형 변형과 지지 해제. 전부 제외.',
'C05_N07_both_palms':'단목 근육형 변형 및 양손 지지 해제, 후기 흉부 연기. 전부 제외.',
'C05_N08_longneck':'0.75~2초 작은 추가 팔, 3.5초 지지 해제, 4~5초 디졸브. 전부 제외.'}
for e in g['entries']:
 u=e['unit_id'];ok=u in accepted and not(u=='C02_K05_shortchain' and e['take']==1)
 if ok:
  interval,note=accepted[u]
  e.update(status='ORIGINAL_PRESERVED_SELECTED',recommended_interval=interval,review={'status':'SELECTED_IN_FINAL_EDIT','note':note,'scope':'실제 원본/최종본 추출 프레임 독립·교차 검수. 실청취·실시간 연속재생 미검증.'})
 else:e.update(status='ORIGINAL_PRESERVED_HOLD',recommended_interval=None,review={'status':'HOLD_DO_NOT_USE','note':holds[u],'scope':'실제 추출 프레임에서 결함 확인. 원본 보존.'})
 if u=='C05_N08_longneck':e.update(end_frame='inputs/C05_N08_longneck_end.png',generation_mode='Frames start and end')
 if e.get('end_frame'):e['end_frame_sha256']=hashlib.sha256((P/e['end_frame']).read_bytes()).hexdigest()
write(P/'generation_log.json',g)
d=json.loads((P/'task_status.json').read_text(encoding='utf-8-sig'))
d.update(user_stated_credits=250,known_balance_at_start={'current_u0':50,'current_u1':0,'current_u2':50,'current_u3':50,'current_u4':50},observed_start_total=200,latest_observed_balances={f'current_u{i}':0 for i in range(5)},observed_success_net_credits=200,pending_generation_requests=0,selected_new_originals=6,held_new_originals=6,updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
d['final_u0_observation']='계정 패널 Google Flow 크레딧 0개 직접 관측. flow_completed_u0_final.png.'
d['balance_discrepancy_note']='사용자250과 실제5계정최초관측합계200의50차이는 미해명. 250사용 또는 남은50으로 표시하지 않는다.'
d['requests']=[{k:e.get(k) for k in ['unit_id','take','asset_id','project_url','model','cost_displayed','balance_before','balance_after','status']} for e in g['entries']]
d['preserved_originals']=[{k:e.get(k) for k in ['original','asset_id','sha256','status']} for e in g['entries']]
d['final_edit_candidates']={f'C{i:02}':f'C{i:02}'+('_r3' if i==5 else '')+f'/C{i:02}_Q-AI_Fair_final_v13.mp4' for i in range(1,7)}
d['final_review_status']='6편 실제 추출 프레임 독립3인·교차·최종재확인 완료. 필수 미해결0. 실청취·현장상영 미검증.'
write(P/'task_status.json',d)
print('Preserved',len(g['entries']),'selected6/hold6, credits200, remaining0')
