# Import modules ===============================================================
import pandas as pd
import matplotlib.pyplot as plt


result_folder = 'plot_results'

# Load data ====================================================================
df_diff = pd.read_csv('cv_percent_results/CNV_diff.csv', index_col = 0)
df_diff_2 = pd.read_csv('cv_percent_results/CNV_diff_2.csv', index_col = 0)


# # Plot figures =================================================================
# fig, axes = plt.subplots(2, 3, figsize = (18, 12))

# df_diff_2.plot(kind='scatter', x='Diploid_diff', y='Gain_diff', color = 'red', ax=axes[0, 0], alpha = 0.5)
# axes[0, 0].set_title('Diploid_diff vs Gain_diff')
# axes[0, 0].set_xlabel('Diploid_diff (%)')
# axes[0, 0].set_ylabel('Gain_diff (%)')
# axes[0, 0].grid(True)

# df_diff_2.plot(kind='scatter', x='Diploid_diff', y='Del_diff', color = 'blue', ax=axes[0, 1], alpha = 0.5)
# axes[0, 1].set_title('Diploid_diff vs Del_diff')
# axes[0, 1].set_xlabel('Diploid_diff (%)')
# axes[0, 1].set_ylabel('Del_diff (%)')
# axes[0, 1].grid(True)

# df_diff_2.plot(kind='scatter', x='Gain_diff', y='Del_diff', color = 'green', ax=axes[0, 2], alpha = 0.5)
# axes[0, 2].set_title('Gain_diff vs Del_diff')
# axes[0, 2].set_xlabel('Gain_diff (%)')
# axes[0, 2].set_ylabel('Del_diff (%)')
# axes[0, 2].grid(True)

# df_diff.plot(kind='scatter', x='0_diff', y='2_diff', color = 'red', ax=axes[1, 0], alpha = 0.5)
# axes[1, 0].set_title('0_diff vs 2')
# axes[1, 0].set_xlabel('0_diff (%)')
# axes[1, 0].set_ylabel('2_diff (%)')
# axes[1, 0].grid(True)

# df_diff.plot(kind='scatter', x='0_diff', y='-2_diff', color = 'blue', ax=axes[1, 1], alpha = 0.5)
# axes[1, 1].set_title('0_diff vs -2')
# axes[1, 1].set_xlabel('0_diff (%)')
# axes[1, 1].set_ylabel('-2_diff (%)')
# axes[1, 1].grid(True)

# df_diff.plot(kind='scatter', x='2_diff', y='-2_diff', color = 'green', ax=axes[1, 2], alpha = 0.5)
# axes[1, 2].set_title('2_diff vs -2_diff')
# axes[1, 2].set_xlabel('2_diff (%)')
# axes[1, 2].set_ylabel('-2_diff (%)')
# axes[1, 2].grid(True)

# 그래프 그리기 =====================================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Diploid_diff vs Gain_diff에 대한 산점도 함수 정의
def plot_scatter(data, x_col, y_col, color, ax, title, xlabel, ylabel):
    data.plot(kind='scatter', x=x_col, y=y_col, color=color, ax=ax, alpha=0.5)
    ax.set_title(title, fontsize = 24, fontweight = 'bold', pad = 20)
    ax.set_xlabel(xlabel, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.grid(True)

# 각 산점도에 대한 설정 정의
plot_configs = [
    (df_diff_2, 'Diploid_diff', 'Gain_diff', 'red', axes[0, 0], 'Diploid_diff vs Gain_diff', 'Diploid_diff (%)', 'Gain_diff (%)'),
    (df_diff_2, 'Diploid_diff', 'Del_diff', 'blue', axes[0, 1], 'Diploid_diff vs Del_diff', 'Diploid_diff (%)', 'Del_diff (%)'),
    (df_diff_2, 'Gain_diff', 'Del_diff', 'green', axes[0, 2], 'Gain_diff vs Del_diff', 'Gain_diff (%)', 'Del_diff (%)'),
    (df_diff, '0_diff', '2_diff', 'red', axes[1, 0], '0_diff vs 2', '0_diff (%)', '2_diff (%)'),
    (df_diff, '0_diff', '-2_diff', 'blue', axes[1, 1], '0_diff vs -2', '0_diff (%)', '-2_diff (%)'),
    (df_diff, '2_diff', '-2_diff', 'green', axes[1, 2], '2_diff vs -2_diff', '2_diff (%)', '-2_diff (%)')
]

# 각 산점도 그리기
for config in plot_configs:
    plot_scatter(*config)


# 그래프 표시
# plt.show()


# Save as png and pdf ==========================================================

plt.tight_layout()
plt.savefig(f'{result_folder}/CNV_diff_scatter.png', format='png', dpi=300)
plt.savefig(f'{result_folder}/CNV_diff_scatter.pdf', format='pdf', dpi=300)


# Make a 3D figure =============================================================
import plotly.express as px

fig = px.scatter_3d(
    df_diff_2,
    x = 'Diploid_diff',
    y = 'Del_diff',
    z = 'Gain_diff',
    title = 'Diploid vs Gain vs Deletion',
    labels = {'Diploid_diff': 'Diploid_diff', 'Del_diff': 'Del_diff', 'Gain_diff': 'Gain_diff'},
    size_max = 1,
    # color_discrete_sequence
)
fig.write_html(f'{result_folder}/CNV_diff_3D_1.html')

fig2 = px.scatter_3d(
    df_diff,
    x = '0_diff',
    y = '-2_diff',
    z = '2_diff',
    title = 'Diploid vs Gain vs Deletion',
    labels = {'0_diff': '0_diff', '-2_diff': '-2_diff', '2_diff': '2_diff'},
    size_max = 1,
    # color_discrete_sequence
)
fig2.write_html(f'{result_folder}/CNV_diff_3D_2.html')