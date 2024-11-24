import mygene
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# MyGene API를 통해 유전자 정보 가져오기 함수
def process_gene_file(file_path, color, label):
    # 유전자 리스트 준비
    gene_list = pd.read_csv(file_path)
    gene_list = gene_list['Gene Symbol'].tolist()

    # MyGene API 호출
    mg = mygene.MyGeneInfo()
    query = mg.querymany(gene_list, scopes='symbol', fields='chrom,genomic_pos', species='human')
    df = pd.DataFrame(query)

    # 유효한 'genomic_pos' 필드만 남김
    df = df.dropna(subset=['genomic_pos'])

    # 'notfound' 컬럼 제거
    if 'notfound' in df.columns:
        df = df.drop(columns=['notfound'])

    # 'genomic_pos' 필드에서 필요한 값 추출
    def filter_and_flatten(genomic_loc):
        if isinstance(genomic_loc, list):
            filtered = [d for d in genomic_loc if not d.get('chr', '').startswith('H')]
            return filtered[0] if filtered else None
        elif isinstance(genomic_loc, dict):
            return genomic_loc
        return None

    df['genomic_pos'] = df['genomic_pos'].apply(filter_and_flatten)
    df = df.dropna(subset=['genomic_pos'])

    df['chrom'] = df['genomic_pos'].apply(lambda x: x.get('chr', None))
    df['start'] = df['genomic_pos'].apply(lambda x: x.get('start', None))

    # 크로모좀 데이터를 정렬 가능한 카테고리로 변환
    chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y']
    df['chrom'] = pd.Categorical(df['chrom'], categories=chromosomes, ordered=True)

    # 색상 및 레이블 정보 추가
    df['color'] = color
    df['label'] = label

    return df

# 세 개의 CSV 파일 처리
df1 = process_gene_file("./extracted_genesets/gain_geneset.csv", color="red", label="Gain")
df2 = process_gene_file("./extracted_genesets/del_geneset.csv", color="blue", label="Del")
df3 = process_gene_file("./extracted_genesets/mdel_pgain.csv", color="green", label="mDel_pGain")

# 데이터 병합
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# 시각화
plt.figure(figsize=(12, 8))
sns.stripplot(
    data=combined_df,
    x='chrom', y='start', hue='label',
    jitter=True, size=7, alpha=0.7,
    palette={'Gain': 'red', 'Del': 'blue', 'mDel_pGain': 'green'})

# x축 및 y축 설정
chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y']
plt.xticks(
    ticks=range(len(chromosomes)),
    labels=chromosomes,
    rotation=45,
    fontsize=16
)
plt.yticks(fontsize=16)

# 그래프 제목과 축 이름 설정
plt.title('Chromosomal Distribution of Genes', fontsize=20, fontweight='bold')
plt.xlabel('Chromosome', fontsize=18)
plt.ylabel('Genomic Position (bp)', fontsize=18)

# 범례 추가
plt.legend(title='Files', fontsize=14, title_fontsize=16)

plt.tight_layout()
plt.show()
