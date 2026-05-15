'''CODING HOMEWORK #4'''
'''Rachel Papirmeister'''
'''UNI: rmp2205'''

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from matplotlib import colormaps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Classifiers():
    def __init__(self, data):
        X = data[['A', 'B']].values
        y = data['label'].values

        # split 60% training & 40% testing
        self.training_data, self.testing_data, self.training_labels, self.testing_labels = \
            train_test_split(X, y, test_size=0.4, random_state=42)

        self.outputs = []

    def test_clsf(self, clsf, classifier_name=''):
        # Fit the classifier (GridSearchCV already fits on training data)
        clsf.fit(self.training_data, self.training_labels)

        # Best training score from cross-validation
        best_train_score = clsf.best_score_

        # Test score on held-out test set
        test_score = clsf.score(self.testing_data, self.testing_labels)

        best_params = clsf.best_params_

        print(f"  Best params: {best_params}")
        print(f"  Best CV training score: {best_train_score:.4f}")
        print(f"  Test score: {test_score:.4f}")


        self.outputs.append(f"{classifier_name}, {best_train_score:.4f}, {test_score:.4f}")

        self.plot(self.testing_data, self.testing_labels, model=clsf.best_estimator_, classifier_name=classifier_name)

    def classifyNearestNeighbors(self):
        param_grid = {'n_neighbors': list(range(1, 20, 2)), 'leaf_size': list(range(5, 35, 5))}

        clsf = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)
        self.test_clsf(clsf, classifier_name='KNeighborsClassifier')

    def classifyLogisticRegression(self):
        param_grid = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}

        clsf = GridSearchCV(LogisticRegression(max_iter=1000), param_grid, cv=5)
        self.test_clsf(clsf, classifier_name='LogisticRegression')

    def classifyDecisionTree(self):
        param_grid = {'max_depth': list(range(1, 51)), 'min_samples_split': list(range(2, 11))}

        clsf = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=5)
        self.test_clsf(clsf, classifier_name='DecisionTreeClassifier')

    def classifyRandomForest(self):
        param_grid = {'max_depth': list(range(1, 6)), 'min_samples_split': list(range(2, 11))}

        clsf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5)
        self.test_clsf(clsf, classifier_name='RandomForestClassifier')

    def classifyAdaBoost(self):
        param_grid = {'n_estimators': list(range(10, 80, 10))}
        
        clsf = GridSearchCV(AdaBoostClassifier(random_state=42), param_grid, cv=5)
        self.test_clsf(clsf, classifier_name='AdaBoostClassifier')

    def plot(self, X, Y, model, classifier_name=''):
        X1 = X[:, 0]
        X2 = X[:, 1]

        X1_min, X1_max = min(X1) - 0.5, max(X1) + 0.5
        X2_min, X2_max = min(X2) - 0.5, max(X2) + 0.5

        X1_inc = (X1_max - X1_min) / 200.
        X2_inc = (X2_max - X2_min) / 200.

        X1_surf = np.arange(X1_min, X1_max, X1_inc)
        X2_surf = np.arange(X2_min, X2_max, X2_inc)
        X1_surf, X2_surf = np.meshgrid(X1_surf, X2_surf)

        L_surf = model.predict(np.c_[X1_surf.ravel(), X2_surf.ravel()])
        L_surf = L_surf.reshape(X1_surf.shape)

        plt.figure()
        plt.title(classifier_name)
        plt.contourf(X1_surf, X2_surf, L_surf, cmap=plt.cm.coolwarm, zorder=1)
        plt.scatter(X1, X2, s=38, c=Y)
        plt.margins(0.0)
        plt.savefig(f'{classifier_name}.png', dpi=150, bbox_inches='tight')
        plt.show()
        plt.close()


if __name__ == "__main__":
    df = pd.read_csv('input.csv')

    plt.figure()
    plt.title('Dataset Scatter Plot')
    plt.scatter(df[df['label'] == 0]['A'], df[df['label'] == 0]['B'], marker='o', label='Class 0')
    plt.scatter(df[df['label'] == 1]['A'], df[df['label'] == 1]['B'], marker='^', label='Class 1')
    plt.xlabel('A')
    plt.ylabel('B')
    plt.legend()
    plt.savefig('dataset_scatter.png', dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()

    models = Classifiers(df)

    print('Classifying with KNN ☺')
    models.classifyNearestNeighbors()
    print('Classifying with Logistic Regression ☺')
    models.classifyLogisticRegression()
    print('Classifying with Decision Tree ☺')
    models.classifyDecisionTree()
    print('Classifying with Random Forest ☺')
    models.classifyRandomForest()
    print('Classifying with AdaBoost ☺')
    models.classifyAdaBoost()

    with open("output.csv", "w") as f:
        print('Name, Best Training Score, Testing Score', file=f)
        for line in models.outputs:
            print(line, file=f)

    print('\nDone! Check output.csv for results.')