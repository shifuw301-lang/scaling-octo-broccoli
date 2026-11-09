import pandas as pd
import re

df = pd.read_csv("pubmed_extract_full.csv")

anti_keywords = [
    "anti-inflammatory", "reduce inflammation", "decrease tnf",
    "inhibit inflammatory", "alleviate inflammation", "suppress inflammation",
    "downregulate tnf", "attenuate inflammation"
]
pro_keywords = [
    "pro-inflammatory", "induce inflammation", "increase tnf",
    "promote inflammatory", "trigger inflammation", "exacerbate inflammation",
    "upregulate tnf"
]

def label_inflammation(abstract):
    # 核心修复：全部转为字符串，空值变成 ""
    text = str(abstract).lower()
    is_anti = any(k in text for k in anti_keywords)
    is_pro = any(k in text for k in pro_keywords)
    if is_anti and not is_pro:
        return "anti"
    elif is_pro and not is_anti:
        return "pro"
    else:
        return ""

df["inflammation_label"] = df["Abstract"].apply(label_inflammation)

df.to_csv("pubmed_labeled.csv", index=False, encoding="utf-8-sig")

print("✅ 炎症标签打标完成，输出 pubmed_labeled.csv")
print(f"抗炎文献数量：{ (df['inflammation_label'] == 'anti').sum() }")
print(f"促炎文献数量：{ (df['inflammation_label'] == 'pro').sum() }")

