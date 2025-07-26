import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
import numpy as np

# بارگذاری داده‌ها
df = pd.read_csv("data_generation1.csv")

# ساخت ستون گروه ترکیبی
df['Group'] = df['FatherDiet'].astype(str) + "_" + df['OffspringDiet'].astype(str) + "_" + df['Exercise'].astype(str)

st.title("📊 داشبورد تحلیلی نسل دوم")

# انتخاب گروه و متغیر
groups = df['Group'].unique()
group_sel = st.selectbox("🔍 انتخاب گروه:", groups)

numeric_vars = df.select_dtypes(include='number').columns.tolist()
var_sel = st.selectbox("📈 انتخاب متغیر:", numeric_vars)

# زیرمجموعه فیلتر شده
sub_df = df[df['Group'] == group_sel][var_sel].dropna()

# آمار توصیفی
if len(sub_df) < 2:
    st.warning("📉 داده کافی برای رسم نمودار وجود ندارد.")
else:
    st.subheader("📌 آمار توصیفی")
    mean = sub_df.mean()
    std = sub_df.std()
    sk = skew(sub_df)
    n = sub_df.count()

    st.write(f"**میانگین (μ):** {mean:.2f}")
    st.write(f"**انحراف معیار (σ):** {std:.2f}")
    st.write(f"**چولگی:** {sk:.2f}")
    st.write(f"**تعداد:** {n}")

    # 📊 رسم نمودار
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(sub_df, kde=True, stat='density', bins=int(np.sqrt(n)),
                 color='cornflowerblue', edgecolor='black', alpha=0.6, ax=ax)
    ax.axvline(mean, color='red', linestyle='--')
    ax.set_title(f"{var_sel} - گروه {group_sel}")
    st.pyplot(fig)
