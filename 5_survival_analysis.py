# Import libraries =============================================================
import pandas as pd
import numpy as np
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import matplotlib.patheffects as PathEffects

# Pathes =======================================================================
clinicalDataPath = '/home/jsw/BI/Database/Glioma_clinical/'
result_path = 'survival_results/'



# //==========================================================================//
# //                                                                          //
# //                              FUNCTIONS                                   //
# //                                                                          //
# //==========================================================================//
def survival_analysis(merged_df, geneset):
    # :merged_df: Each row is a sample and each column is a gene expression
    # values with and clinical informations
    # :geneset: A list of genes to analyze
    # :return: A dataframe with log-rank test results and long survival group
    
    # make a new dataframe with only the genes in the geneset ==================
    result_df = pd.DataFrame(index=geneset,
                            columns=['log_rank', 'p_value', 'long_survival'])
    result_df[:] = np.nan   # fill the dataframe with NaN
    
    for gene in geneset:
        upper_quartile_threshold = merged_df[gene].quantile(0.75)
        lower_quartile_threshold = merged_df[gene].quantile(0.25)
        high_df = merged_df[merged_df[gene] >= upper_quartile_threshold]
        low_df = merged_df[merged_df[gene] <= lower_quartile_threshold]
        
        median_high = high_df['OS'].median()
        median_low = low_df['OS'].median()
        
        result = logrank_test(low_df['OS'],
                        high_df['OS'],
                        event_observed_A = low_df['Censor'],
                        event_observed_B = high_df['Censor'])

        result_df.at[gene, 'log_rank'] = result.test_statistic
        result_df.at[gene, 'p_value'] = result.p_value
        
        if median_high > median_low:
            result_df.at[gene, 'long_survival'] = 'high'
        elif median_high < median_low:
            result_df.at[gene, 'long_survival'] = 'low'
        else:
            result_df.at[gene, 'long_survival'] = 'same'
            
    return result_df

def plotting_and_analysis (result_df, cut_off=0.01, filename='', format='pdf'):
    # Modify the result_df for plotting ========================================
    df_plot = result_df[result_df['long_survival'] != 'same'].copy()
    df_plot.loc[df_plot['long_survival'] == 'low', 'log_rank'] *= -1
    df_top = df_plot.sort_values(by = 'log_rank', ascending = False).head(20)
    df_bot = df_plot.sort_values(by = 'log_rank', ascending = True).head(20)
    df_text = pd.concat([df_top, df_bot]).drop_duplicates()

    # Plotting =================================================================
    plt.figure(figsize=(6.6, 6))
    sns.scatterplot(
        x='log_rank',
        y=-np.log10(df_plot['p_value'].astype(float)),
        data=df_plot,
        hue='long_survival',
        # style='long_survival',
        s=100,
        palette={'high': 'firebrick', 'low': 'royalblue'})

    # Set cut off ==============================================================
    _cut_off = -np.log10(cut_off)

    # y <= cutoff인 점을 회색으로 변경 (사실 덮어 씌우는 거임)
    for i in range(len(df_plot)):
        x = df_plot['log_rank'].iloc[i]
        y = -np.log10(df_plot['p_value'].astype(float)).iloc[i]
        if y <= _cut_off:
            plt.scatter(x, y, color='lightgray', s=100)

    # y = cutoff인 선 추가
    plt.axhline(y=_cut_off, color='gray', linestyle='--')

    # Add texts (gene names) ===================================================
    texts = []
    for i in range(len(df_text)):
        x = df_text['log_rank'].iloc[i]
        y = -np.log10(df_text['p_value'].astype(float)).iloc[i]
        text = plt.text(x, y, df_text.index[i], fontsize=9, color='black')
        text.set_path_effects([
            PathEffects.Stroke(linewidth=3, foreground='white'),
            PathEffects.Normal()])
        texts.append(text)

    # adjust_text를 이용하여 텍스트가 서로 겹치지 않도록 조정
    adjust_text(texts, arrowprops = dict(arrowstyle='-', color='gray', lw=0.7))

    # Set labels ===============================================================
    plt.xlabel('log rank')
    plt.ylabel('-log10(p_value)')
    plt.title(f'Log-rank test for {filename}')
    plt.legend(title='long survival',loc = 'lower left')

    # save the plot as pdf =====================================================
    plt.savefig(f'{result_path}{filename}.pdf',
                format=format, bbox_inches='tight')


# //==========================================================================//
# //                                                                          //
# //                                CODES                                     //
# //                                                                          //
# //==========================================================================//


# Load clinical data ===========================================================
tcga_clinical = pd.read_csv(f'{clinicalDataPath}TCGA_mRNAseq_702_clinical.txt',
                            sep='\t', index_col = 0)
tcga_clinical = tcga_clinical.dropna(subset = ['Grade', 'OS'])

tcga_genes = pd.read_csv(f'{clinicalDataPath}TCGA_mRNAseq_702.txt', sep='\t',
                         index_col = 0).T
tcga_genes = tcga_genes.loc[tcga_clinical.index]

merged_df = pd.merge(tcga_clinical, tcga_genes,
                     left_index = True, right_index = True)

# keep rows with grade IV
gbm_df = merged_df[merged_df['Grade'] == 'Grade IV']



# Load geneset to analyze (GAIN) ===============================================
geneset = pd.read_csv('extracted_genesets/gain_geneset.csv')

# make a list of genes in the geneset and header of the merged_df
geneset_list = list(geneset['Gene Symbol'])
header_list = list(merged_df.columns)

# maintain the genes in the geneset and the  header of the merged_df
geneset_intersect = [gene for gene in geneset_list if gene in header_list]

# Perform survival analysis ====================================================
result_df = survival_analysis(merged_df, geneset_intersect)
result_df.to_csv(f'{result_path}survival_gain_tcga_glioma.csv')
plotting_and_analysis(result_df, filename='survival_gain_tcga_glioma')

result_df = survival_analysis(gbm_df, geneset_intersect)
result_df.to_csv(f'{result_path}survival_gain_tcga_gbm.csv')
plotting_and_analysis(result_df, cut_off=0.05,
                      filename='survival_gain_tcga_gbm')





# Load geneset to analyze (DELETION) ===========================================
geneset = pd.read_csv('extracted_genesets/del_geneset.csv')

# make a list of genes in the geneset and header of the merged_df
geneset_list = list(geneset['Gene Symbol'])
header_list = list(merged_df.columns)

# maintain the genes in the geneset and the  header of the merged_df
geneset_intersect = [gene for gene in geneset_list if gene in header_list]

# Perform survival analysis ====================================================
result_df = survival_analysis(merged_df, geneset_intersect)
result_df.to_csv(f'{result_path}survival_del_tcga_glioma.csv')
plotting_and_analysis(result_df, filename='survival_del_tcga_glioma')

result_df = survival_analysis(gbm_df, geneset_intersect)
result_df.to_csv(f'{result_path}survival_del_tcga_gbm.csv')
plotting_and_analysis(result_df, cut_off=0.05,
                      filename='survival_del_tcga_gbm')





# Load geneset to analyze (mdel_pgain) =========================================
geneset = pd.read_csv('extracted_genesets/mdel_pgain.csv')

# make a list of genes in the geneset and header of the merged_df
geneset_list = list(geneset['Gene Symbol'])
header_list = list(merged_df.columns)

# maintain the genes in the geneset and the  header of the merged_df
geneset_intersect = [gene for gene in geneset_list if gene in header_list]

# Perform survival analysis ====================================================
result_df = survival_analysis(merged_df, geneset_intersect)
result_df.to_csv(f'{result_path}survival_mdel_pgain_tcga_glioma.csv')
plotting_and_analysis(result_df, filename='survival_mdel_pgain_tcga_glioma')

result_df = survival_analysis(gbm_df, geneset_intersect)
result_df.to_csv(f'{result_path}survival_mdel_pgain_tcga_gbm.csv')
plotting_and_analysis(result_df, cut_off=0.05,
                      filename='survival_mdel_pgain_tcga_gbm')

