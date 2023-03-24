import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA


st.title(''' web apps clusterint kmeans \n''')

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


data = pd.read_csv("penguins_size.csv")
data1 = data.dropna()
data2 = data1.iloc[:,2:6]
data3 = data2.values.reshape(-1,2)
X = np.array(data3)

print(X)
print(X.shape)

cluster_slider = st.slider(
    min_value = 1, max_value = 6, value=2, label = "kmeans cluster:"
)
kmeans = KMeans(n_clusters=cluster_slider,random_state=2022).fit(X)
labels = kmeans.labels_

select1 = st.selectbox("",[False,True])
select2 = st.selectbox("standard deviation :", [1, 2, 3])

warna = ['red','seagreen','orange','blue','yellow','purple']

label =len(set(labels))

individu = st.selectbox("subplot individual",[False,True])

if individu:
    fig,ax = plt.subplots(n_cols=label)
else:
    fig,ax = plt.subplots()
for i, yi in enumerate(set(labels)):
    if not individu:
        a = ax
    else:
        a = ax[i]
    xi = X[labels == yi]
    x_pts = xi[:,0]
    y_pts = xi[:,1]

    a.scatter(x_pts , y_pts, c=warna[yi])

    if select1:
        confidence_ellipse(
            x=x_pts,
            y=y_pts,
            a=ax,
            edgecolor="black",
            facecolor=warna[yi],
            alpha=0.2,
            n_std = select2
        )

plt.tight_layout()
st.write(fig)