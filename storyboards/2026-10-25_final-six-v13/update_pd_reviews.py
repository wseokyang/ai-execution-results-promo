raise SystemExit('Historical intermediate updater. Final selections are in generation_log.json and reviews/final_film_review.json.')
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
f=P/'generation_log.json'
d=json.loads(f.read_text(encoding='utf-8'))
review={
'C01_K06_pose_bridge_take01':('PD_CONDITIONAL_SELECT',[.5,4],'코치가 누운 상태에서 팔·다리를 올림. 이후 높은 자세에 맞춰 후속 새 컷 사용.'),
'C04_K01_note_push_take01':('PD_CONDITIONAL_SELECT',[.5,5.5],'동일 종이가 안으로 들어가고 빈손이 빠짐.'),
'C05_N05_hand_transfer_take01':('PD_CONDITIONAL_SELECT',[2,5.5],'앞을 잡던 한 손이 지붕 아래로 이동. 회전 완료 아님.'),
'C01_K07_lower_back_take01':('HOLD',None,'코치가 사라지고 두 몸이 합쳐짐. 누움 인서트로 분리 재설계.'),
'C02_K05_shortchain_take01':('HOLD',None,'손을 떼며 수갑 고리가 세 개로 증식.'),
'C05_N06_pivot_take01':('PD_CONDITIONAL_SELECT',[1.5,5.5],'실제 목 빼기와 정면 회전. 지지손이 잠깐 떨어짐; 연속 하중 지지 성공으로 주장하지 않음. 다음 양손 받침 필요.'),
'C02_K05_shortchain_take02':('PD_CONDITIONAL_SELECT',[.5,5],'두 고리 유지, 손 이탈과 반응 확보. 긴 사슬의 기존 K06 제외.'),
'C04_K08_hinges_take01':('PD_CONDITIONAL_SELECT',[1,4],'세 창문 실제 열림, 정확 세 인물.'),
'C01_K07_close_recline_take01':('PD_CONDITIONAL_SELECT',[.75,4.5],'단독 근접으로 등·머리 바닥까지 내림. 몸 겹침 없음.')
}
ends={'C02_K05_shortchain_take02':'C02_K05_end_two_cuffs.png','C04_K08_hinges_take01':'C04_K08_open_target.png'}
for e in d['entries']:
 key=e['unit_id']+'_take'+str(e['take']).zfill(2)
 if key in review:
  state,span,note=review[key];e['review']={'status':state,'proposed_source_interval':span,'note':note,'scope':'PD actual 0.5s contact sheets and selected full PNGs; continuous playback/audio listening not performed; independent final edit review pending'}
 if key in ends:
  ep=P/'inputs'/ends[key];e['end_frame']='inputs/'+ends[key];e['end_frame_sha256']=hashlib.sha256(ep.read_bytes()).hexdigest();e['generation_mode']='Frames start and end'
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
s=json.loads((P/'task_status.json').read_text(encoding='utf-8'))
s['requests']=[{'unit':e['unit_id'],'take':e['take'],'model':e['model'],'cost_displayed':e['cost_displayed'],'balance_before':e['balance_before'],'balance_after':e['balance_after'],'asset_id':e['asset_id'],'project_url':e['project_url'],'status':'ORIGINAL_PRESERVED'} for e in d['entries']]
s['last_verified_account_balances']={'current_u3':0,'current_u4':0,'current_u2':0}
s['unverified_accounts']=['current_u0','current_u1']
(P/'task_status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
