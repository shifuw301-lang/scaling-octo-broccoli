import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from matplotlib.ticker import MultipleLocator

# ===================== 中文设置 =====================
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===================== 读取千篇提取结果 =====================
df = pd.read_csv("pubmed_extract_result_v2_1000.csv")

# ===================== 关键词 → 中文翻译对照表 =====================
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

# ===================== 关键词统计函数 =====================
def count_keyword(col):
    all_words = []
    for s in df[col].dropna():
        if s != "":
            all_words.extend(s.split(";"))
    return Counter(all_words)

# 各个字段统计
model_cnt = count_keyword("model")
organ_cnt = count_keyword("organ")
cytokine_cnt = count_keyword("cytokine")
source_cnt = count_keyword("source")
disease_cnt = count_keyword("disease")

# ===================== 画布 一行5个子图 =====================
fig, axes = plt.subplots(1, 5, figsize=(24, 7))

# ===================== 绘图函数（柱子顶部标数字 + Y轴宽松刻度） =====================
def draw_bar(ax, counter, title):
    items = counter.most_common()
    # 英文关键词、数量
    en_names, nums = zip(*items)
    # 翻译成中文标签
    cn_names = [trans[name] for name in en_names]

    bars = ax.bar(cn_names, nums)
    ax.set_title(title, fontsize=13)

    # X轴文字倾斜
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=11)

    # Y轴刻度：间隔100
    ax.yaxis.set_major_locator(MultipleLocator(100))

    # ✅ 在每根柱子顶端写上文献数量
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 8, f"{h}", ha="center", fontsize=10)

# 依次画5张图
draw_bar(axes[0], model_cnt, "实验模型")
draw_bar(axes[1], organ_cnt, "靶器官")
draw_bar(axes[2], cytokine_cnt, "炎症因子")
draw_bar(axes[3], source_cnt, "β葡聚糖来源")
draw_bar(axes[4], disease_cnt, "疾病模型")

# 自动排版，防止文字被截断
plt.tight_layout()

# 保存高清图片
plt.savefig("beta_glucan_stat_cn_1000.png", dpi=300)
plt.show()
print("✅ 绘图完成！图片：beta_glucan_stat_cn_1000.png")

