import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import imageio

# 결과 저장 폴더 생성 =============================================================
result_folder = "plot_results"
os.makedirs(result_folder, exist_ok=True)

# 데이터 로드 =====================================================================
df_diff_2 = pd.read_csv('cv_percent_results/CNV_diff_2.csv', index_col=0)

# 3D 그래프 생성 함수 ============================================================
def create_3d_scatter(data, x, y, z, title):
    """
    축의 면을 숨기고 보라색 점으로 3D 산점도를 생성, 투명도 추가
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=data[x],
        y=data[y],
        z=data[z],
        mode='markers',
        marker=dict(size=5, color='purple', opacity=0.7)  # 보라색 점 + 투명도
    ))
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(title=x, backgroundcolor="rgba(0,0,0,0)", showgrid=False),
            yaxis=dict(title=y, backgroundcolor="rgba(0,0,0,0)", showgrid=False),
            zaxis=dict(title=z, backgroundcolor="rgba(0,0,0,0)", showgrid=False),
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig

# 첫 번째 그래프 생성
fig1 = create_3d_scatter(df_diff_2, 'Diploid_diff', 'Del_diff', 'Gain_diff', 'Diploid vs Gain vs Deletion')

# 프레임 생성 함수 ================================================================
def make_gif_frames(fig, num_frames=180):
    """
    3D 그래프를 일정 각도로 회전하며 프레임 생성 (메모리에 저장)
    """
    images = []
    for i in range(num_frames):
        angle = i * (360 / num_frames)  # 프레임마다 회전 각도 계산
        fig.update_layout(scene_camera=dict(
            eye=dict(
                x=np.sin(np.radians(angle)) * 3,  # x 값을 작게 설정하여 각도를 낮춤
                y=np.cos(np.radians(angle)) * 3,  # y 값을 작게 설정하여 각도를 낮춤
                z=0  # z 값을 낮게 설정하여 높이 조정
            )
        ))
        images.append(fig.to_image(format="png", width=800, height=600))
    return images

# 첫 번째 그래프 GIF 생성
frames_1 = make_gif_frames(fig1, num_frames=180)
with imageio.get_writer(f"{result_folder}/CNV_diff_3D_1_rotation.gif", mode='I', duration=0.03) as writer:
    for frame in frames_1:
        writer.append_data(imageio.imread(frame))

# MP4 저장을 위한 함수 ============================================================
def save_mp4(frames, output_path):
    """
    imageio를 사용하여 MP4 동영상 저장
    """
    with imageio.get_writer(output_path, fps=30, codec="libx264") as writer:
        for frame in frames:
            writer.append_data(imageio.imread(frame))

# 첫 번째 그래프 MP4 저장
save_mp4(frames_1, f"{result_folder}/CNV_diff_3D_1_rotation.mp4")

print("GIF 및 MP4 생성 완료! 결과는 plot_results 폴더에 저장되었습니다.")
