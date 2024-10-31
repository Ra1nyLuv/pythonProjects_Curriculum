import numpy as np
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB 
from sklearn import model_selection
from sklearn.metrics import f1_score

### STEP1 ###
# 加载数据
input_file = r'Machine_Learning_Projects\experiment3\adult.data.txt'  # adult.data.txt'
X = []
y = []
num_lessthan50k = 0
num_morethan50k = 0
num_threshold = 30000
with open(input_file, 'r') as f:
    for line in f.readlines():
        if '?' in line:
            continue
        data = line[:-1].split(', ')
        if data[-1] == '<=50K' and num_lessthan50k < num_threshold:
            X.append(data)
            num_lessthan50k += 1
        elif data[-1] == '>50K' and num_morethan50k < num_threshold:
            X.append(data)
            num_morethan50k += 1
        if num_lessthan50k >= num_threshold and num_morethan50k >= num_threshold:
            break
X = np.array(X)

### STEP2 ###
label_encoder = [] 
X_encoded = np.empty(X.shape, dtype=object)
for i, item in enumerate(X[0]):
    if item.isdigit(): 
        X_encoded[:, i] = X[:, i].astype(int)
    else:
        le = preprocessing.LabelEncoder()
        label_encoder.append(le)
        X_encoded[:, i] = le.fit_transform(X[:, i])

X = X_encoded[:, :-1].astype(int)
y = X_encoded[:, -1].astype(int)

### STEP3 ###
# 创建分类器并进行训练
# 交叉验证
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25, random_state=5)
classifier_gaussiannb = GaussianNB()
classifier_gaussiannb.fit(X_train, y_train)
y_test_pred = classifier_gaussiannb.predict(X_test)

# 计算F1得分
f1 = f1_score(y_test, y_test_pred, average='weighted')
print("F1 score: " + str(round(100 * f1, 2)) + "%")

### STEP4 ###
# 创建个例，将其进行同样编码处理
input_data = ['39', 'State-gov', '77516', 'Bachelors', '13', 'Never-married', 'Adm-clerical', 'Not-in-family', 'White', 'Male', '2174', '0', '40', 'United-States'] 
count = 0
input_data_encoded = [-1] * len(input_data)
for i, item in enumerate(input_data):
    if item.isdigit():
        input_data_encoded[i] = int(item)
    else:
        input_data_encoded[i] = int(label_encoder[count].transform([item])[0])  # 提取数组的第一个元素
        count += 1 
input_data_encoded = np.array(input_data_encoded)

# 确保特征数量一致
input_data_features = input_data_encoded 
output_class = classifier_gaussiannb.predict([input_data_features])
print("Predicted class: " + label_encoder[-1].inverse_transform(output_class)[0])