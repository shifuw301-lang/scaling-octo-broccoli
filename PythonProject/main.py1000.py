from Bio import Entrez
import time
import pandas as pd

Entrez.email = "shifuw301@gmail.com"
query = "(beta-glucan) AND (inflammation)"

# 查询一共有多少篇文献
handle = Entrez.esearch(db="pubmed", term=query, retmax=0)
record = Entrez.read(handle)
total = int(record["Count"])
print(f"这个关键词一共检索到：{total} 篇文献")

download_num = min(total, 1000)
print(f"准备下载 {download_num} 篇")

# 获取文献编号列表
handle = Entrez.esearch(db="pubmed", term=query, retmax=download_num)
record = Entrez.read(handle)
pmid_list = record["IdList"]

data = []
batch = 200
# 分批拉取
for i in range(0, len(pmid_list), batch):
    batch_pmid = pmid_list[i:i+batch]
    print(f"正在下载第 {i+1} ~ {i+len(batch_pmid)} 篇")
    handle = Entrez.efetch(db="pubmed", id=batch_pmid, rettype="medline", retmode="xml")
    articles = Entrez.read(handle)["PubmedArticle"]
    for art in articles:
        med = art["MedlineCitation"]
        pmid = med["PMID"]
        title = med["Article"]["ArticleTitle"]
        abstract = ""
        if "Abstract" in med["Article"]:
            abs_list = med["Article"]["Abstract"]["AbstractText"]
            abstract = " ".join([str(x) for x in abs_list])
        data.append({"PMID":pmid, "Title":title, "Abstract":abstract})
    time.sleep(1)

# 保存，文件名带1000，✅不会碰你原来100篇的文件
df = pd.DataFrame(data)
df.to_csv("pubmed_beta_glucan_1000.csv", index=False, encoding="utf-8-sig")
print("✅ 下载完毕，文件 pubmed_beta_glucan_1000.csv 生成")
