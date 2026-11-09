import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# 读取新版本提取结果！注意文件名改成v2
df = pd.read_csv("pubmed_extract_result_v2.csv")

# 关键词 → 中文翻译对照表
trans = {
    "mouse": "小鼠",
    "mice": "小鼠",
    "rat": "大鼠",
    "cell": "细胞",
    "in vitro": "体外实验",

    "lung": "肺",
    "liver": "肝脏",
    "spleen": "脾脏",
    "intestine": "肠道",

    "TNF-α": "TNF-α",
    "IL-6": "IL-6",
    "IL-10": "IL-10",
    "IL-1β": "IL-1β",

    "yeast": "酵母",
    "mushroom": "蘑菇",
    "oat": "燕麦",

    "liver injury": "肝损伤",
    "colitis": "肠炎",
    "pulmonary injury": "肺损伤"
}

def count_keywords(col_name):
    all_words = []
    for cell in df[col_name]:
        if pd.notna(cell) and cell != "":
            words = cell.split(";")
            all_words.extend(words)
    cnt = Counter(all_words)
    # 英文关键词翻译成中文
    new_cnt = {}
    for k, v in cnt.items():
        new_cnt[trans[k]] = v
    return new_cnt

# 五个维度统计
model_count = count_keywords("model")
organ_count = count_keywords("organ")
cytokine_count = count_keywords("cytokine")
source_count = count_keywords("source")
disease_count = count_keywords("disease")

# 一行5个子图
fig, axes = plt.subplots(1,5,figsize=(22,5))

axes[0].bar(model_count.keys(), model_count.values())
axes[0].set_title("实验模型")
axes[0].set_ylabel("文献篇数")
axes[0].set_yticks(range(0, max(model_count.values())+2, 2))

axes[1].bar(organ_count.keys(), organ_count.values())
axes[1].set_title("靶器官")
axes[1].set_yticks(range(0, max(organ_count.values())+2, 2))

axes[2].bar(cytokine_count.keys(), cytokine_count.values())
axes[2].set_title("炎症因子")
axes[2].set_yticks(range(0, max(cytokine_count.values())+2, 2))

axes[3].bar(source_count.keys(), source_count.values())
axes[3].set_title("β-葡聚糖来源")
axes[3].set_yticks(range(0, max(source_count.values())+2, 2))

axes[4].bar(disease_count.keys(), disease_count.values())
axes[4].set_title("疾病模型")
axes[4].set_yticks(range(0, max(disease_count.values())+2, 2))

plt.tight_layout()
plt.savefig("beta_glucan_stat_cn.png", dpi=300)
plt.show()
print("✅ 中文高清绘图完成，图片保存 beta_glucan_stat_cn.png")
