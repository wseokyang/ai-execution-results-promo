from pathlib import Path
import subprocess,sys
r=Path(__file__).parent
jobs=[
('C04_K01','Soldiers_stuffing_envelope_insid…_20261024231257.mp4','f7adf177-18f4-4bc1-8ee2-28061ebaf051','Soldiers stuffing envelope insid…',110),
('C04_K02','Commander_handing_documents_to_r…_20261024231311.mp4','27a6427d-70ff-4c5e-8b45-64942e0668ff','Commander handing documents to r…',100),
('C04_K03','Commander_blocks_serving_trolley…_20261024231325.mp4','6be8ae95-ae3f-4861-a346-ba70f982d408','Commander blocks serving trolley…',90),
('C04_K04','Person_pointing_at_comparison_pa…_20261024231443.mp4','556b5dde-c2d7-48db-84dd-25d138312292','Person pointing at comparison pa…',80),
('C04_K05','Guard_examining_papers_and_trolley_20261024231457.mp4','0a422b50-27a2-46e8-8dbb-013d52e2c7a8','Guard examining papers and trolley',70),
('C04_K06','Commander_and_guard_by_trolley_20261024231511.mp4','28b50abc-dead-4c8e-bc49-3463bc18829d','Commander and guard by trolley',60)]
for unit,filename,asset,title,before in jobs:
    subprocess.run([sys.executable,'-X','utf8',str(r/'inspect_clip.py'),str(Path('C:/Users/wseok/Downloads')/filename),unit,'--take','1','--asset',asset,'--title',title,'--before',str(before),'--after',str(before-10),'--project','https://flow.google.com/project/0bbf4d01-698f-4ccb-8bb2-231f1d1123b2','--account','current_u0'],check=True,stdout=subprocess.DEVNULL)
    print(unit,'preserved and decoded',flush=True)
