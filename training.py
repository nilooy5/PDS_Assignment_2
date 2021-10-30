from sklearn import datasets, neighbors, metrics, svm
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt


def run_classification(dataset_name, classification_name, number_of_folds, label_best_parameter, label_accuracy):
    if dataset_name == 'iris':
        dataset = datasets.load_iris()
    elif dataset_name == 'breast_cancer':
        dataset = datasets.load_breast_cancer()
    elif dataset_name == 'wine':
        dataset = datasets.load_wine()

    if classification_name == 'KNN':
        classifier = neighbors.KNeighborsClassifier()
        parameter = [{'n_neighbors': range(30)}]
        x_label = 'Value of K for KNN'
    elif classification_name == 'svc':
        classifier = svm.SVC()
        parameter = [{'gamma': [0.0001, 0.001, 0.01, 0.1, 1.0]}]
        x_label = 'Parameter C'

    x = dataset.data
    y = dataset.target
    class_names = dataset.target_names
    X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    gscv_classifier = GridSearchCV(
        estimator=classifier,
        param_grid=parameter,
        cv=number_of_folds,  # k-fold cross validation
        scoring='accuracy'
    )

    gscv_classifier.fit(X_train, Y_train)

    means = gscv_classifier.cv_results_['mean_test_score']
    stds = gscv_classifier.cv_results_['std_test_score']
    results = gscv_classifier.cv_results_['params']

    print("Grid scores on validation set:")
    print()

    for mean, std, param in zip(means, stds, results):
        print("Parameter: %r, accuracy: %0.3f (+/-%0.03f)" % (param, mean, std * 2))
    print()

    label_accuracy.config(
        text='Best parameter: '
             + str(gscv_classifier.best_params_)
             + ' score: {0:.2f}%'.format(gscv_classifier.best_score_)
    )
    print("Best parameter:"
          + str(gscv_classifier.best_params_)
          + ' & accuracy score: {0:.2f}%'.format(gscv_classifier.best_score_))

    y_pred = gscv_classifier.predict(X_test)
    # • Plot confusion matrix and accuracy
    accuracy = metrics.accuracy_score(Y_test, y_pred) * 100
    print('overall accuracy: {0:.2f}%'.format(accuracy))
    label_best_parameter.config(text='Accuracy = {0:.2f}%'.format(accuracy))
    plotcm = metrics.ConfusionMatrixDisplay.from_estimator(gscv_classifier, X_test, Y_test, display_labels=class_names)
    plotcm.ax_.set_title('Accuracy = {0:.2f}%'.format(accuracy))
    plt.show()

    x_axis = list(parameter[0].values())[0]
    y_axis = means
    plot_axes = plt.axes()
    plt.xlabel(x_label)
    plt.ylabel('CV score')
    plot_axes.plot(x_axis, y_axis)
    plt.show()

