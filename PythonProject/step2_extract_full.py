import pandas as pd
import re

# 读取原始文献
df_raw = pd.read_csv("pubmed_beta_glucan_1000.csv")

# 初始化空列表用来保存每一行的标签
animal_list = []
organ_list = []
cytokine_list = []
source_list = []
disease_list = []
mw_list = []          # 分子量 kDa
admin_list = []       # 给药途径

# ========== 关键词字典，后续可以继续扩充 ==========
animal_keywords = {
    "mouse": ["mouse", "mice", "murine"],
    "rat": ["rat"],
    "human": ["human", "patient"],
    "rabbit": ["rabbit"],
    "zebrafish": ["zebrafish"]
}

organ_keywords = {
    "liver": ["liver", "hepatic"],
    "lung": ["lung", "pulmonary"],
    "kidney": ["kidney", "renal"],
    "colon": ["colon"],
    "intestine": ["intestine", "gut"],
    "brain": ["brain", "cerebral"],
    "heart": ["heart", "myocardial"]
}

cytokine_keywords = {
    "TNF-α": ["tnf-α", "tnf alpha", "tnfa"],
    "IL-6": ["il-6", "il 6"],
    "IL-1β": ["il-1β", "il 1 beta"],
    "IFN-γ": ["ifn-γ", "ifn gamma"]
}

source_keywords = {
    "yeast": ["yeast"],
    "oat": ["oat", "oats"],
    "mushroom": ["mushroom"],
    "bacteria": ["bacteria", "bacterial"]
}

disease_keywords = {
    "inflammation": ["inflammation", "inflammatory"],
    "fibrosis": ["fibrosis"],
    "cancer": ["cancer", "carcinoma"],
    "diabetes": ["diabetes"]
}

admin_keywords = {
    "oral": ["oral", "orally"],
    "i.p.": ["intraperitoneal", "i.p."],
    "i.v.": ["intravenous", "i.v."],
    "i.m.": ["intramuscular", "i.m."],
    "topical": ["topical"]
}

# 分子量正则 ✅ 修正完成，去掉 pattern:，加上忽略大小写
mw_pattern = re.compile(r"(\d+\.?\d*)\s*-?kda", re.IGNORECASE)


def match_keywords(text, keyword_dict):
    """通用关键词匹配函数，多个命中用逗号隔开"""
    hit = []
    for label, words in keyword_dict.items():
        for w in words:
            if w.lower() in text.lower():
                hit.append(label)
                break
    return ",".join(hit) if hit else ""


def extract_molecular_weight(text):
    """提取kDa分子量，取第一个匹配到的数值"""
    res = mw_pattern.findall(text)
    if res:
        return float(res[0])
    else:
        return None


# ========== 循环遍历全部文献摘要 ==========
for idx, row in df_raw.iterrows():
    abstract = str(row["Abstract"])

    animal_list.append(match_keywords(abstract, animal_keywords))
    organ_list.append(match_keywords(abstract, organ_keywords))
    cytokine_list.append(match_keywords(abstract, cytokine_keywords))
    source_list.append(match_keywords(abstract, source_keywords))
    disease_list.append(match_keywords(abstract, disease_keywords))
    admin_list.append(match_keywords(abstract, admin_keywords))
    mw_list.append(extract_molecular_weight(abstract))


# 组装成新数据表
df_out = pd.DataFrame({
    "PMID": df_raw["PMID"],
    "Title": df_raw["Title"],
    "Abstract": df_raw["Abstract"],
    "animal": animal_list,
    "organ": organ_list,
    "cytokine": cytokine_list,
    "source": source_list,
    "disease": disease_list,
    "administration": admin_list,
    "molecular_weight_kDa": mw_list
})

# 输出完整特征表
df_out.to_csv("pubmed_extract_full.csv", index=False, encoding="utf-8-sig")
print("✅ 特征提取完成，文件输出：pubmed_extract_full.csv")
print(f"一共处理文献数量：{len(df_out)}")
print(f"成功抓取分子量的文献数：{df_out['molecular_weight_kDa'].notna().sum()}")
print(f"成功抓取给药途径的文献数：{(df_out['administration'] != '').sum()}")

