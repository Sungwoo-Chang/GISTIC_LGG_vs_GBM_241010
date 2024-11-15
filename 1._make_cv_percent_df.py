#===============================================================================
#
#Making -2, -1, 0, 1, 2 percentage dataframe from the GISTIC analysis results
#
#===============================================================================

# Import modules ===============================================================
import pandas as pd
result_folder = 'cv_percent_results'


# Read the GISTIC analysis results =============================================
df_gbm = pd.read_csv('CV_data/GBM_all_thresholded.by_genes.txt', sep='\t', index_col=0)
df_lgg = pd.read_csv('CV_data/LGG_all_thresholded.by_genes.txt', sep='\t', index_col=0)

df_gbm = df_gbm.drop(df_gbm.columns[[0, 1]], axis = 1)
df_lgg = df_lgg.drop(df_lgg.columns[[0, 1]], axis = 1)


# Make raw count dataframe =====================================================
def count_values(row):
    return{
        '-2': (row == -2).sum(),
        '-1': (row == -1).sum(),
        '0': (row == 0).sum(),
        '1': (row == 1).sum(),
        '2': (row == 2).sum()
    }

df_gbm_counts = df_gbm.apply(count_values, axis=1, result_type='expand')
df_gbm_counts['total'] = df_gbm_counts.sum(axis=1)

df_lgg_counts = df_lgg.apply(count_values, axis=1, result_type='expand')
df_lgg_counts['total'] = df_lgg_counts.sum(axis=1)

df_gbm_counts.to_csv(f'{result_folder}/GBM_cnv_counts.csv')
df_lgg_counts.to_csv(f'{result_folder}/LGG_cnv_counts.csv')


# Make percentage dataframe for -2, -1, 0, 1, 2 ================================
df_gbm_pct = df_gbm_counts.div(df_gbm_counts['total'], axis=0)
df_lgg_pct = df_lgg_counts.div(df_lgg_counts['total'], axis=0)

df_gbm_pct = (df_gbm_pct * 100).round(2)
df_lgg_pct = (df_lgg_pct * 100).round(2)

df_gbm_pct.to_csv(f'{result_folder}/GBM_cnv_percentages.csv')
df_lgg_pct.to_csv(f'{result_folder}/LGG_cnv_percentages.csv')


# Make percentage dataframe (Deletion, Diploid, Gain) ==========================
df_gbm_pct_2 = pd.DataFrame({
    'Deletion': df_gbm_pct['-2'] + df_gbm_pct['-1'],
    'Diploid': df_gbm_pct['0'],
    'Gain': df_gbm_pct['1'] + df_gbm_pct['2']
}).round(2)

df_lgg_pct_2 = pd.DataFrame({
    'Deletion': df_lgg_pct['-2'] + df_lgg_pct['-1'],
    'Diploid': df_lgg_pct['0'],
    'Gain': df_lgg_pct['1'] + df_lgg_pct['2']
}).round(2)

df_gbm_pct_2.to_csv(f'{result_folder}/GBM_cnv_percentages_2.csv')
df_lgg_pct_2.to_csv(f'{result_folder}/LGG_cnv_percentages_2.csv')


# Make difference dataframe ====================================================
df_diff = pd.DataFrame({
    '-2_diff': df_gbm_pct['-2'] - df_lgg_pct['-2'],
    '-1_diff': df_gbm_pct['-1'] - df_lgg_pct['-1'],
    '0_diff': df_gbm_pct['0'] - df_lgg_pct['0'],
    '1_diff': df_gbm_pct['1'] - df_lgg_pct['1'],
    '2_diff': df_gbm_pct['2'] - df_lgg_pct['2']
}).round(2)

df_diff_2 = pd.DataFrame({
    'Del_diff': df_gbm_pct_2['Deletion'] - df_lgg_pct_2['Deletion'],
    'Diploid_diff': df_gbm_pct_2['Diploid'] - df_lgg_pct_2['Diploid'],
    'Gain_diff': df_gbm_pct_2['Gain'] - df_lgg_pct_2['Gain']
}).round(2)

df_diff.to_csv(f'{result_folder}/CNV_diff.csv')
df_diff_2.to_csv(f'{result_folder}/CNV_diff_2.csv')