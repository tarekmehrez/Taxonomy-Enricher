"""Contains the plot module."""
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def plot_vector_space(title, vectors, labels):
    """
    Plot a vector space.

    params:
        title (str): title of the saved plot
        vectors (list[float])
        labels (list[str]): labels of each vectors
    """
    low_dim_embs = PCA(n_components=2).fit_transform(vectors)
    plot(low_dim_embs, labels)

    if title:
        output_file = 'fig-%s.eps' % title
        plt.savefig(output_file, format='eps', dpi=1200)
        plt.clf()
    else:
        plt.show()
        plt.clf()


def plot(vectors, labels):
    """
    Plot passed vectors and their labels.

    params:
        vectors (list[float])
        labels (list[str]): labels of each vectors
    """
    for label, x, y in zip(labels, vectors[:, 0], vectors[:, 1]):
        plt.plot(x, y, 'x')
        plt.annotate(label, xy=(x, y))
