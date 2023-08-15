import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

def load_data(file):
    try:
        dataframe = pd.read_csv(file)
        return dataframe
    except Exception as e:
        st.error(f"Ошибка: {e}")
        return None

def plot(dataFrame, column, checkBox):
    distribution_df = dataFrame.dropna(subset=column)
    if checkBox:
        subDataFrame = distribution_df[column].value_counts().nlargest(15).rename_axis('unique_values').reset_index(name='counts')
        fig = px.pie(subDataFrame, values='counts', names='unique_values', title=column)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(distribution_df[column].value_counts().nlargest(15), use_container_width=True)

def hypothesisTest(dataFrame, column1, column2, test):
    st.subheader("Тестирование гипотез")
    if (dataFrame[column1].dtypes != 'object') and (
            dataFrame[column1].dtypes != 'string') and (dataFrame[column2].dtypes != 'object') and (
            dataFrame[column2].dtypes != 'string'):
        if test == "t-критерий Стьюдента":
            stat, p_value = stats.ttest_ind(dataFrame[column1], dataFrame[column2])
            st.write(f"statistic={stat:.4f}")
            st.write(f"p-value={p_value:.4f}")
        elif test == "Критерий хи-квадрат" and dataFrame[column1].dtype == "object":
            contingency_table = pd.crosstab(dataFrame[column1], dataFrame[column2])
            stat, p_value = stats.chi2_contingency(contingency_table)
            st.write(f"statistic={stat:.4f}")
            st.write(f"p-value={p_value:.4f}")
        else:
            stat, p_value = stats.mannwhitneyu(dataFrame[column1], dataFrame[column2])
            st.write(f"statistic={stat:.4f}")
            st.write(f"p-value={p_value:.4f}")
    else:
        st.write(f"Неверный тип данных")


def streamlit_run():
    st.title('Промежуточная аттестация')
    uploaded_file = st.file_uploader("Выберите CSV файл", type='csv')
    if uploaded_file is not None:
        dataFrame = load_data(uploaded_file)
        if dataFrame is not None:
            col1, col2 = st.columns(2)
            with col1:
                column1 = st.selectbox('Выберите колонку 1', dataFrame.columns)
                checkBox1 = st.checkbox('Категориальная переменная', key="1")
                plot(dataFrame, column1, checkBox1)
            with col2:
                column2 = st.selectbox('Выберите колонку 2', dataFrame.columns)
                checkBox2 = st.checkbox('Категориальная переменная', key="2")
                plot(dataFrame, column2, checkBox2)
            selectedHypothesis = st.selectbox("Выберите алгоритм тестирования гипотез",
                                         ["U-критерий Манна — Уитни", "Критерий хи-квадрат", "t-критерий Стьюдента"])
            if st.button("Начать тестирование"):
                hypothesisTest(dataFrame, column1, column2, selectedHypothesis)

if __name__ == '__main__':
    streamlit_run()