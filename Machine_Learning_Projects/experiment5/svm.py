# matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
# import seaborn as sns;
# sns.set()  # 使用seaborn的默认设置

# 0. 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#1. 产生数据
# 随机来点数据  make_blobs为聚类产生数据集
from sklearn.datasets._samples_generator import make_blobs
# center：产生数据的中心点，默认值3
X, y = make_blobs(n_samples=50, centers=2, random_state=0, cluster_std=0.60)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')

plt.title("1. 产生数据")
plt.show()

#2. 画分割线
xfit = np.linspace(-1, 3.5)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
plt.plot([0.6], [2.1], 'x', color='red', markeredgewidth=2, markersize=10)
for m, b in [(1, 0.65), (0.5, 1.6), (-0.2, 2.9)]:
    plt.plot(xfit, m * xfit + b, '-k')
plt.xlim(-1, 3.5)

plt.title("2. 画分割线")
plt.show()

#3. 画隔离带
xfit = np.linspace(-1, 3.5)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
for m, b, d in [(1, 0.65, 0.33), (0.5, 1.6, 0.55), (-0.2, 2.9, 0.2)]:
    yfit = m * xfit + b
    plt.plot(xfit, yfit, '-k')
    plt.fill_between(xfit, yfit - d, yfit + d, edgecolor='none',
                     color='#AAAAAA', alpha=0.4)  # alpha透明度
plt.xlim(-1, 3.5);
plt.title("3. 画隔离带")
plt.show()

#4. 训练支持向量机
plt.subplots();
from sklearn.svm import SVC # "Support vector classifier"支持向量机的一个分类器
model = SVC(kernel='linear', C=1E10)##核函数选用线性分类
model.fit(X, y)###开始训练一个基本的SVM
def plot_svc_decision_function(model, ax=None, plot_support=True):
    """Plot the decision function for a 2D SVC"""
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # create grid to evaluate model创建网格来评估模型
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y, x)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)

    # plot decision boundary and margins  # 画决策边界和边缘
    ax.contour(X, Y, P, colors='k',
               levels=[-1, 0, 1], alpha=0.5,
               linestyles=['--', '-', '--'])

    # plot support vectors画支持向量
    if plot_support:
        ax.scatter(model.support_vectors_[:, 0],
                   model.support_vectors_[:, 1],
                   s=300, linewidth=1, facecolors='none');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
plot_svc_decision_function(model);
plt.title("4. 训练支持向量机")
plt.show()

#5. 改变数据点的个数
def plot_svm(N=10, ax=None):
    X, y = make_blobs(n_samples=200, centers=2,
                      random_state=0, cluster_std=0.60)
    X = X[:N]
    y = y[:N]
    model = SVC(kernel='linear', C=1E10)
    model.fit(X, y)

    ax = ax or plt.gca()
    ax.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 6)
    plot_svc_decision_function(model, ax)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
for axi, N in zip(ax, [60, 120]):  # 改变数据的个数【60，120】，只要支持向量不变，决策边界就不改变'''
    plot_svm(N, axi)
    axi.set_title('N = {0}'.format(N))
plt.show()

#6. 引入线性核函数
plt.subplots();
from sklearn.datasets._samples_generator import make_circles  ###重新构造数据集
X, y = make_circles(100, factor=.1, noise=.1) ###圆环型的数据集

clf = SVC(kernel='linear').fit(X, y)##先采用线性的SVM

plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
plot_svc_decision_function(clf, plot_support=False);
plt.title("6. 引入线性核函数")
plt.show()

#7. 从二维变三维
from mpl_toolkits import mplot3d
r = np.exp(-(X ** 2).sum(1))
def plot_3D(elev=30, azim=30, X=X, y=y):
    ax = plt.subplot(projection='3d')
    ax.scatter3D(X[:, 0], X[:, 1], r, c=y, s=50, cmap='autumn')
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('r')

plot_3D(elev=45, azim=45, X=X, y=y)
plt.title("7. 从二维变三维")
plt.show()


#8. 加入径向基函数
#加入径向基函数（就是高斯核函数或者rbf核函数），都是高斯变换
clf = SVC(kernel='rbf', C=1E6)
clf.fit(X, y)

plt.subplots();
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
plot_svc_decision_function(clf)
plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
            s=300, lw=1, facecolors='none');
plt.title("8. 加入径向基函数")
plt.show()

#9. 需要软间隔的数据
X, y = make_blobs(n_samples=100, centers=2,
                  random_state=0, cluster_std=0.8)
plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn');
plt.title("9. 需要软间隔的数据")
plt.show()

#10. 不同C下容忍程度不一样
X, y = make_blobs(n_samples=100, centers=2,
                  random_state=0, cluster_std=0.8)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)

###改变C参数的大小对结果的影响，可以看到，C太大划分更严格，泛化能力更弱，适合要求

###C小，要求越放松。

###通常用交叉验证来评判哪个效果好，就取哪个C
for axi, C in zip(ax, [10.0, 0.1]):#分别取得ax，10；ax，0.1赋给axi，C然后执行循环。
    model = SVC(kernel='linear', C=C).fit(X, y)
    axi.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
    plot_svc_decision_function(model, axi)
    axi.scatter(model.support_vectors_[:, 0],
                model.support_vectors_[:, 1],
                s=300, lw=1, facecolors='none');
    axi.set_title('C = {0:.1f}'.format(C), size=14)
plt.show()

#11. 不同gamma下模型复杂度不一样
X, y = make_blobs(n_samples=100, centers=2,
                  random_state=0, cluster_std=1.1)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
#####探究高斯核函数中的gamma系数：
#####   控制模型的一些复杂程度，
#####   越大的gamma值，表示映射的维度越高，模型越复杂，可能会让所有点都成了支持向量
#####   越小，模型越精简，结果更平稳。所以精度并不能直接说明模型好坏

for axi, gamma in zip(ax, [10.0, 0.1]):
    model = SVC(kernel='rbf', gamma=gamma).fit(X, y)
    axi.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
    plot_svc_decision_function(model, axi)
    axi.scatter(model.support_vectors_[:, 0],
                model.support_vectors_[:, 1],
                s=300, lw=1, facecolors='none');
    axi.set_title('gamma = {0:.1f}'.format(gamma), size=14)
print("")
plt.show()