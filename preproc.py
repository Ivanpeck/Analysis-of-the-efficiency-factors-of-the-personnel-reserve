import pandas as pd



df = pd.read_excel('без лишнего_Россия_Эффективность.xlsx')
# Загружаем данные (у вас уже есть df)
target = "Оцените эффективность работы вашего кадрового резерва с точки зрения бизнес-эффекта/ вклада в развитие компании по шкале от 0 до 10, (где 0 – совсем неэффективен, 10 – очень эффективен)"

# Уберем строки с пропусками по ключевому столбцу (у вас их нет, но на всякий случай)
df = df.dropna(subset=[target,'Как выглядит механизм планирования потребности в кадровый резерв в вашей компании?'])

for col in df.columns[1:-1]:
    df.loc[df[col].fillna('').str.contains('Затруд')| df[col].fillna('').str.contains('Другое') ,col] = pd.NA

charact_points = {
    1:{
        'name':'высок',
        'matching condition': lambda series: series>=8,
    },
    -1:{
        'name':'низк',
        'matching condition': lambda series: series<=5,
    }
}

# Кодируем категориальные переменные
X = pd.get_dummies(df.drop(columns=['id сессии',target]), dummy_na=False).astype(int)

# Целевая переменная
y_plus1 = charact_points[1]['matching condition'](df[target]).astype(int)
y_minus1 = charact_points[-1]['matching condition'](df[target]).astype(int)

X_y = X.copy()
X_y['y'] = y_plus1
X_y.to_excel('X_y для R_plus1.xlsx',index=False)
X_y['y'] = y_minus1
X_y.to_excel('X_y для R_minus1.xlsx',index=False)

X.to_excel('X.xlsx',index=False)