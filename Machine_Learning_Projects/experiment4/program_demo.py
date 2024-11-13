from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.svm import SVC

# 加载数据集
digits = load_digits()
X, y = digits.data, digits.target

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 决策树分类器
dt_clf = DecisionTreeClassifier(criterion='gini', max_depth=None, max_features=None)
dt_clf.fit(X_train, y_train)
y_pred_dt = dt_clf.predict(X_test)
print("决策树分类准确率:", accuracy_score(y_test, y_pred_dt))

# 随机森林分类器
rf_clf = RandomForestClassifier(n_estimators=100, criterion='gini', max_depth=None, max_features='sqrt', random_state=42)
rf_clf.fit(X_train, y_train)
y_pred_rf = rf_clf.predict(X_test)
print("随机森林分类准确率:", accuracy_score(y_test, y_pred_rf))

# 调整随机森林参数
rf_tuned_clf = RandomForestClassifier(n_estimators=200, criterion='entropy', max_depth=10, max_features='log2', random_state=42)
rf_tuned_clf.fit(X_train, y_train)
y_pred_rf_tuned = rf_tuned_clf.predict(X_test)
print("调整后的随机森林分类准确率:", accuracy_score(y_test, y_pred_rf_tuned))

# 使用ExtraTreesClassifier
et_clf = ExtraTreesClassifier(n_estimators=100, random_state=42)
et_clf.fit(X_train, y_train)
y_pred_et = et_clf.predict(X_test)
print("ExtraTrees分类准确率:", accuracy_score(y_test, y_pred_et))

# 使用AdaBoostClassifier
ada_clf = AdaBoostClassifier(n_estimators=100, algorithm='SAMME', random_state=42)
ada_clf.fit(X_train, y_train)
y_pred_ada = ada_clf.predict(X_test)
print("AdaBoost分类准确率:", accuracy_score(y_test, y_pred_ada))

# 使用BaggingClassifier
bag_clf = BaggingClassifier(estimator=SVC(), n_estimators=10, random_state=42)
bag_clf.fit(X_train, y_train)
y_pred_bag = bag_clf.predict(X_test)
print("Bagging分类准确率:", accuracy_score(y_test, y_pred_bag))