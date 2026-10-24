from pathlib import Path
import subprocess,sys
r=Path(__file__).parent
jobs=[('C04_K08',2,'Three_adults_waiting_with_bowls_20261024232741.mp4','495fab14-c62a-4918-97bb-000616f8f83e','Three adults waiting with bowls',50,40),('C01_K03',1,'Man_pressing_laptop_playback_key_20261024232754.mp4','c5848b2a-9ab4-4658-aabd-dbee5942a091','Man pressing laptop playback key',40,30),('C01_K04',1,'Man_falling_from_rolling_chair_20261024232807.mp4','917ecc09-1b38-453f-acde-ab0cba7d60a5','Man falling from rolling chair',30,20)]
for unit,take,filename,asset,title,before,after in jobs:
 subprocess.run([sys.executable,'-X','utf8',str(r/'inspect_clip.py'),str(Path('C:/Users/wseok/Downloads')/filename),unit,'--take',str(take),'--asset',asset,'--title',title,'--before',str(before),'--after',str(after),'--project','https://flow.google.com/u/1/project/296632f8-cb96-4214-b962-85d5fc522ffa','--account','current_u1'],check=True,stdout=subprocess.DEVNULL)
 print(unit,'preserved',flush=True)
