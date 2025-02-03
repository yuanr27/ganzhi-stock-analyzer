import streamlit as st
from datetime import datetime

# 预置预测规则表（示例日期数据直接硬编码）
PREDICTION_RULES = {
    # 格式：日期字符串: [干支组合, 火气强度, 走势类型, 风险等级]
    "2025-01-14": ["乙巳年 丁丑月 癸未日", 2, "低开震荡走高", "中"],
    "2025-01-27": ["乙巳年 丁丑月 丙申日", 3, "冲高回落", "高"],
    "2025-02-05": ["乙巳年 戊寅月 乙巳日", 4, "跳空缺口不回补", "极高"],
    "2025-02-19": ["乙巳年 戊寅月 己未日", 2, "阴阳交替震荡", "中"]
}

def main():
    st.title("📈 干支股市分析器（精准版）")
    date_input = st.date_input("选择日期", datetime(2025,1,14), 
                             min_value=datetime(2025,1,1), 
                             max_value=datetime(2025,12,31))
    
    if st.button("立即预测"):
        date_str = date_input.strftime("%Y-%m-%d")
        result = PREDICTION_RULES.get(date_str, None)
        
        if result:
            st.success(f"### {date_str} 预测结果")
            st.write(f"**干支组合**: {result[0]}")
            st.write(f"**火气强度**: {'★'*result[1]}")
            st.write(f"**走势类型**: {result[2]}")
            st.write(f"**风险等级**: {result[3]}")
        else:
            st.warning("该日期暂无预测数据")

if __name__ == "__main__":
    main()
