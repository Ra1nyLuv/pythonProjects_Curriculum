import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, fetch_lfw_people
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# 生成第一组数据
X1, y1 = make_blobs(n_samples=100, centers=2, random_state=0, cluster_std=0.8)

# 划分训练集和测试集
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

# 寻找合适的C值
C_values = [0.1, 1, 10, 100]
best_score_linear = 0
best_C_linear = None
for C in C_values:
    model_linear = SVC(kernel='linear', C=C)
    model_linear.fit(X1_train, y1_train)
    score = model_linear.score(X1_test, y1_test)
    if score > best_score_linear:
        best_score_linear = score
        best_C_linear = C

# 使用最佳C值训练最终模型
final_model_linear = SVC(kernel='linear', C=best_C_linear)
final_model_linear.fit(X1, y1)

# 生成第二组数据
X2, y2 = make_blobs(n_samples=100, centers=2, random_state=0, cluster_std=1.1)

# 划分训练集和测试集
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)

# 寻找合适的gamma值
gamma_values = [0.1, 1, 10, 100]
best_score_rbf = 0
best_gamma_rbf = None
for gamma in gamma_values:
    model_rbf = SVC(kernel='rbf', gamma=gamma)
    model_rbf.fit(X2_train, y2_train)
    score = model_rbf.score(X2_test, y2_test)
    if score > best_score_rbf:
        best_score_rbf = score
        best_gamma_rbf = gamma

# 使用最佳gamma值训练最终模型
final_model_rbf = SVC(kernel='rbf', gamma=best_gamma_rbf)
final_model_rbf.fit(X2, y2)

# 加载人脸数据集
lfw_people = fetch_lfw_people(min_faces_per_person=60)
X_lfw = lfw_people.data
y_lfw = lfw_people.target

# 划分训练集和测试集
X_lfw_train, X_lfw_test, y_lfw_train, y_lfw_test = train_test_split(X_lfw, y_lfw, test_size=0.2, random_state=42)

# 定义参数网格
param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [0.1, 1, 10, 100]}
model_lfw = SVC(kernel='rbf')
grid_search = GridSearchCV(model_lfw, param_grid)
grid_search.fit(X_lfw_train, y_lfw_train)

# 获取最佳参数和最佳模型
best_C_lfw = grid_search.best_params_['C']
best_gamma_lfw = grid_search.best_params_['gamma']
final_model_lfw = SVC(kernel='rbf', C=best_C_lfw, gamma=best_gamma_lfw)
final_model_lfw.fit(X_lfw, y_lfw)

# 使用t-SNE对人脸数据集进行降维可视化
tsne = TSNE(n_components=2, random_state=42)
X_lfw_tsne = tsne.fit_transform(X_lfw)

# 在降维后的数据上训练新的模型用于绘制决策边界
final_model_lfw_tsne = SVC(kernel='rbf', C=best_C_lfw, gamma=best_gamma_lfw)
final_model_lfw_tsne.fit(X_lfw_tsne, y_lfw)

# 绘制决策边界函数
def plot_decision_boundary(model, X, y):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=20, edgecolor='k')

# 可视化第一组数据的决策边界
plt.figure(figsize=(8, 6))
plot_decision_boundary(final_model_linear, X1, y1)
plt.title('Linear SVM on First Dataset (C={})'.format(best_C_linear))
plt.show()

# 可视化第二组数据的决策边界
plt.figure(figsize=(8, 6))
plot_decision_boundary(final_model_rbf, X2, y2)
plt.title('RBF SVM on Second Dataset (gamma={})'.format(best_gamma_rbf))
plt.show()

# 可视化LFW数据集的决策边界
plt.figure(figsize=(8, 6))
plot_decision_boundary(final_model_lfw_tsne, X_lfw_tsne, y_lfw)
plt.title('RBF SVM on LFW Dataset (C={}, gamma={})'.format(best_C_lfw, best_gamma_lfw))
plt.show()