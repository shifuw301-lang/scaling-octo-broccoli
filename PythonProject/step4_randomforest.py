import pandas as pd
import matplotlib.pyplot as plt
# 解决中文方框乱码
plt.rcParams['font.sans-serif'] = ['SimHei']   # 黑体
plt.rcParams['axes.unicode_minus'] = False    # 负号正常显示





from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import MultiLabelBinarizer

# ---------------------- 1.读取打标后的数据 ----------------------
df = pd.read_csv("pubmed_labeled.csv")
# 只保留有炎症标签 anti / pro 的行
df = df[df["inflammation_label"].isin(["anti", "pro"])].reset_index(drop=True)
print(f"用于建模的总样本数：{len(df)}")

# 特征列
feature_cols = ["animal", "organ", "source", "administration", "cytokine"]

# 多标签二值化函数：增加前缀，防止列名重复
def multi_encode(series, prefix_name):
    list_data = series.apply(lambda s: str(s).split(",") if str(s)!="" else [])
    mlb = MultiLabelBinarizer()
    arr = mlb.fit_transform(list_data)
    col_names = [f"{prefix_name}_{c}" for c in mlb.classes_]
    return pd.DataFrame(arr, columns=col_names), mlb

# 全部特征合并成一张大表
X_list = []
for col in feature_cols:
    one_hot_df, _ = multi_encode(df[col], prefix_name=col)
    X_list.append(one_hot_df)
X = pd.concat(X_list, axis=1)

# Y标签：anti→0，pro→1
y = df["inflammation_label"].map({"anti":0, "pro":1})
print(f"特征总维度：{X.shape[1]}")

# ---------------------- 2.划分训练集、测试集 ----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------- 3.随机森林训练 ----------------------
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# ---------------------- 4.模型评估 ----------------------
y_pred = rf.predict(X_test)
print("\n===== 模型准确率 =====")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print("\n===== 分类报告 =====")
print(classification_report(y_test, y_pred, target_names=["anti(抗炎)","pro(促炎)"]))

# 混淆矩阵绘图
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["anti(抗炎)","pro(促炎)"])
disp.plot(cmap=plt.cm.Blues)
plt.title("混淆矩阵")
plt.savefig("confusion_matrix.png", dpi=300)
plt.close()

# ---------------------- 5.特征重要性绘图 ----------------------
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_
}).sort_values("importance", ascending=False).head(15) #取前15最重要特征

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(10,7))
plt.barh(feature_importance["feature"], feature_importance["importance"])
plt.gca().invert_yaxis()
plt.xlabel("特征重要性")
plt.title("Top15 特征重要性（随机森林预测β葡聚糖炎症效果）")
plt.tight_layout()
plt.savefig("rf_feature_importance.png", dpi=300)
plt.show()

print("\n✅ 绘图完成！")
print("图片1：rf_feature_importance.png 特征重要性")
print("图片2：confusion_matrix.png 混淆矩阵")
print("\nTop15最重要特征：")
print(feature_importance)

