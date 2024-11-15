# Import modules ===============================================================
import pandas as pd
result_folder = 'extracted_genesets'

# Load data ====================================================================
df_diff_2 = pd.read_csv('cv_percent_results/CNV_diff_2.csv', index_col = 0)
df_diff = pd.read_csv('cv_percent_results/CNV_diff.csv', index_col = 0)


gain_geneset = df_diff_2[df_diff_2['Gain_diff'] > 40]
del_geneset = df_diff_2[df_diff_2['Del_diff'] > 45]

p2_geneset = df_diff[df_diff['2_diff'] > 15]    # plus 2
m2_geneset = df_diff[df_diff['-2_diff'] > 15]   # minus 2

mdel_pgain = df_diff_2[(df_diff_2['Gain_diff'] > 20) & (df_diff_2['Del_diff'] < -20)]

# Save genesets to csv =========================================================
gain_geneset.to_csv(f'{result_folder}/gain_geneset.csv')
del_geneset.to_csv(f'{result_folder}/del_geneset.csv')
p2_geneset.to_csv(f'{result_folder}/p2_geneset.csv')
m2_geneset.to_csv(f'{result_folder}/m2_geneset.csv')
mdel_pgain.to_csv(f'{result_folder}/mdel_pgain.csv')

