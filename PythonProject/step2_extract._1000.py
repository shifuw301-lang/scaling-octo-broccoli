import pandas as pd

# 读取原始
df = pd.read_csv("pubmed_beta_glucan_1000.csv")

# ========== 关键词字典【新增 source、disease】 ==========
keyword_dict = {
    "model": ["mouse", "mice", "rat", "cell", "in vitro"],
    "organ": ["lung", "liver", "spleen", "intestine"],
    "cytokine": ["TNF-α", "IL-6", "IL-10", "IL-1β"],
    "source": ["yeast", "mushroom", "oat"],
    "disease": ["liver injury", "colitis", "pulmonary injury"]
}

for idx, row in df.iterrows():
    abstract = str(row["Abstract"]).lower()
    for cate, word_list in keyword_dict.items():
        hit_words = []
        for w in word_list:
            # 全部转小写匹配，防止大小写漏检
            if w.lower() in abstract:
                hit_words.append(w)
        df.at[idx, cate] = ";".join(hit_words)

# 删掉全部关键词都没命中的无效文献
df = df[ ~((df["model"]=="") & (df["organ"]=="") & (df["cytokine"]=="") & (df["source"]=="") & (df["disease"]=="")) ]

# 保存新结果
df.to_csv("pubmed_extract_result_v2_1000.csv", index=False, encoding="utf-8-sig")
print("✅ 关键词提取完成，保存到 pubmed_extract_result_v2.csv")
print(f"筛选后还剩下 {len(df)} 篇有效文献")

