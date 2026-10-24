from pathlib import Path
import subprocess,sys
r=Path(__file__).parent
jobs=[
('Trainee_and_coach_walking_together_20261024233407.mp4','C01_K05',2,'9e6bf8b7-9f9f-488c-a8a4-301e5dd9651c','Trainee and coach walking together',10,0,1,'296632f8-cb96-4214-b962-85d5fc522ffa'),
('Coach_falls_from_rolling_chair_20261024233422.mp4','C01_K06',1,'d19ba919-c972-4649-ab64-1355a8a45e54','Coach falls from rolling chair',10,0,1,'296632f8-cb96-4214-b962-85d5fc522ffa'),
('Coach_and_photographer_on_mat_20261024233442.mp4','C01_K07',1,'4a0d2e24-ec9a-44e3-9a28-e71189dbb108','Coach and photographer on mat',50,40,2,'8e8bf74a-6faf-4d21-bfc0-f3ebacfc9a2c'),
('Coach_and_trainee_on_mat_20261024233455.mp4','C01_K08',1,'8a6f328f-965f-49e8-a58c-7feeeb9d3981','Coach and trainee on mat',40,30,2,'8e8bf74a-6faf-4d21-bfc0-f3ebacfc9a2c'),
('Coach_and_trainee_holding_poses_20261024233509.mp4','C01_K09',1,'6d6e60aa-768f-45f6-b82c-3abf1f85a82c','Coach and trainee holding poses',30,20,2,'8e8bf74a-6faf-4d21-bfc0-f3ebacfc9a2c')]
for file,unit,take,asset,title,before,after,acc,project in jobs:
 subprocess.run([sys.executable,'-X','utf8',str(r/'inspect_clip.py'),f'C:/Users/wseok/Downloads/{file}',unit,'--take',str(take),'--asset',asset,'--title',title,'--before',str(before),'--after',str(after),'--project',f'https://flow.google.com/u/{acc}/project/{project}','--account',f'current_u{acc}'],check=True)
