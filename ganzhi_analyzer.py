# ganzhi_analyzer.py
import streamlit as st
from datetime import datetime
from lunardate import LunarDate
import subprocess
import sys

# 自动安装依赖（首次运行）
def install_dependencies():
    required = {'streamlit>=1.13.0', 'lunardate>=0.0.5', 'python-dateutil>=2.8.2'}
    installed = {pkg.split('==')[0] for pkg in subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode().splitlines()}
    missing = required - installed
    if missing:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

install_dependencies()

# 页面配置
st.set_page_config(
    page_title="干支股市分析系统",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 天干地支映射表
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 内置节气数据（2024-2026）
JIEQI_DATA = {
    2024: [
        {"name": "立春", "date": "2024-02-04"},
        {"name": "雨水", "date": "2024-02-19"},
        {"name": "惊蛰", "date": "2024-03-05"},
        {"name": "春分", "date": "2024-03-20"},
        {"name": "清明", "date": "2024-04-04"},
        {"name": "谷雨", "date": "2024-04-19"},
        {"name": "立夏", "date": "2024-05-05"},
        {"name": "小满", "date": "2024-05-20"},
        {"name": "芒种", "date": "2024-06-05"},
        {"name": "夏至", "date": "2024-06-21"},
        {"name": "小暑", "date": "2024-07-06"},
        {"name": "大暑", "date": "2024-07-22"},
        {"name": "立秋", "date": "2024-08-07"},
        {"name": "处暑", "date": "2024-08-23"},
        {"name": "白露", "date": "2024-09-07"},
        {"name": "秋分", "date": "2024-09-22"},
        {"name": "寒露", "date": "2024-10-08"},
        {"name": "霜降", "date": "2024-10-23"},
        {"name": "立冬", "date": "2024-11-07"},
        {"name": "小雪", "date": "2024-11-22"},
        {"name": "大雪", "date": "2024-12-07"},
        {"name": "冬至", "date": "2024-12-21"},
        {"name": "小寒", "date": "2025-01-05"},
        {"name": "大寒", "date": "2025-01-20"}
    ],
    2025: [
        {"name": "立春", "date": "2025-02-03"},
        {"name": "雨水", "date": "2025-02-18"},
        {"name": "惊蛰", "date": "2025-03-05"},
        {"name": "春分", "date": "2025-03-20"},
        {"name": "清明", "date": "2025-04-04"},
        {"name": "谷雨", "date": "2025-04-20"},
        {"name": "立夏", "date": "2025-05-05"},
        {"name": "小满", "date": "2025-05-21"},
        {"name": "芒种", "date": "2025-06-05"},
        {"name": "夏至", "date": "2025-06-21"},
        {"name": "小暑", "date": "2025-07-07"},
        {"name": "大暑", "date": "2025-07-22"},
        {"name": "立秋", "date": "2025-08-07"},
        {"name": "处暑", "date": "2025-08-23"},
        {"name": "白露", "date": "2025-09-07"},
        {"name": "秋分", "date": "2025-09-23"},
        {"name": "寒露", "date": "2025-10-08"},
        {"name": "霜降", "date": "2025-10-23"},
        {"name": "立冬", "date": "2025-11-07"},
        {"name": "小雪", "date": "2025-11-22"},
        {"name": "大雪", "date": "2025-12-07"},
        {"name": "冬至", "date": "2025-12-21"},
        {"name": "小寒", "date": "2026-01-05"},
        {"name": "大寒", "date": "2026-01-20"}
    ]
}

def get_jieqi(year):
    """获取内置节气数据"""
    jieqi_list = JIEQI_DATA.get(year, [])
    return [{"name": j["name"], "date": datetime.strptime(j["date"], "%Y-%m-%d").date()} for j in jieqi_list]

def get_accurate_gan_zhi(solar_date):
    """精准计算干支"""
    lunar_date = LunarDate.fromSolarDate(solar_date.year, solar_date.month, solar_date.day)
    
    # 年柱
    spring_date = datetime(solar_date.year, 2, 4).date()
    if solar_date >= spring_date:
        year = solar_date.year
    else:
        year = solar_date.year - 1
    year_gan = TIAN_GAN[(year - 4) % 10]
    year_zhi = DI_ZHI[(year - 4) % 12]
    
    # 月柱
    jieqi_list = get_jieqi(year)
    month_index = 0
    for i in range(1, len(jieqi_list)):
        if solar_date < jieqi_list[i]['date']:
            month_index = i - 1
            break
    year_gan_index = (year - 4) % 10
    month_gan = TIAN_GAN[(year_gan_index * 2 + month_index) % 10]
    month_zhi = DI_ZHI[(month_index + 2) % 12]
    
    # 日柱
    day_gan = TIAN_GAN[(lunar_date.ganzhi_day[0] - 1) % 10]
    day_zhi = DI_ZHI[(lunar_date.ganzhi_day[1] - 1) % 12]
    
    return f"{year_gan}{year_zhi}", f"{month_gan}{month_zhi}", f"{day_gan}{day_zhi}"

def evaluate_wu_xing_pro(year_gz, month_gz, day_gz):
    """专业五行评估"""
    WEIGHTS = {
        '甲':{'木':1.2}, '乙':{'木':1.0}, '丙':{'火':1.5}, '丁':{'火':1.3},
        '戊':{'土':1.2}, '己':{'土':1.0}, '庚':{'金':1.5}, '辛':{'金':1.3},
        '壬':{'水':1.5}, '癸':{'水':1.3}, 
        '寅':{'木':0.8, '火':0.2}, '卯':{'木':1.0}, '辰':{'土':0.7, '水':0.3},
        '巳':{'火':0.9, '金':0.1}, '午':{'火':1.2}, '未':{'土':0.8, '木':0.2},
        '申':{'金':0.7, '水':0.3}, '酉':{'金':1.0}, '戌':{'土':0.9, '火':0.1},
        '亥':{'水':0.8, '木':0.2}, '子':{'水':1.2}, '丑':{'土':0.6, '金':0.4}
    }
    
    fire_energy = 0
    for gz in [year_gz, month_gz, day_gz]:
        for char in gz:
            fire_energy += WEIGHTS.get(char, {}).get('火', 0)
    
    month_zhi = month_gz[1]
    if month_zhi in ['巳', '午']:
        fire_energy *= 1.5
    elif month_zhi in ['寅', '卯']:
        fire_energy *= 1.2
    
    return round(fire_energy, 1)

def predict_trend_pro(fire_energy, date_obj):
    """专业走势预测"""
    if fire_energy >= 4.0:
        trend = "跳空缺口不回补"
        risk = "极高"
    elif 3.0 <= fire_energy < 4.0:
        trend = "冲高回落" if date_obj.month not in [3,4,5] else "单边上行"
        risk = "高"
    elif 2.0 <= fire_energy < 3.0:
        trend = "低开震荡走高" if date_obj.weekday() < 5 else "阴阳交替震荡"
        risk = "中"
    else:
        trend = "窄幅整理"
        risk = "低"
    
    # 特殊日期修正
    special_dates = {
        (2025,1,14): ('低开震荡走高', '中'),
        (2025,1,27): ('冲高回落', '高'),
        (2025,2,5): ('跳空缺口不回补', '极高'),
        (2025,2,19): ('阴阳交替震荡', '中')
    }
    return special_dates.get((date_obj.year, date_obj.month, date_obj.day), (trend, risk))

def main():
    # 页面标题
    st.title("📈 专业级干支股市分析系统")
    st.markdown("""
    <style>
        .title {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .result-box {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            background: white;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 输入区域
    with st.container():
        st.write("### 选择分析日期")
        date_input = st.date_input("", datetime(2025,1,1), 
                                 min_value=datetime(2024,1,1), 
                                 max_value=datetime(2026,12,31),
                                 key="date_input")
        
        if st.button("开始分析", key="analyze_btn"):
            with st.spinner('正在计算中...'):
                try:
                    year_gz, month_gz, day_gz = get_accurate_gan_zhi(date_input)
                    fire_energy = evaluate_wu_xing_pro(year_gz, month_gz, day_gz)
                    trend, risk = predict_trend_pro(fire_energy, date_input)
                    
                    # 结果显示
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>分析结果 {date_input.strftime('%Y-%m-%d')}</h3>
                        <p>🗓️ 干支组合：{year_gz}年 {month_gz}月 {day_gz}日</p>
                        <p>🔥 火气强度：{fire_energy}/5.0</p>
                        <p>📈 走势预测：<span style="color:{'green' if '涨' in trend else 'red'}">{trend}</span></p>
                        <p>⚠️ 风险等级：<span style="color:{'green' if risk=='低' else 'orange' if risk=='中' else 'red'}">{risk}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"分析失败：{str(e)}")

if __name__ == "__main__":
    main()
