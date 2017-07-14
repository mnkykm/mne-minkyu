import numpy as np


class ScoringAUC():
    """Score AUC for multiclass problems.
    Average of one against all.
    """
    def __call__(self, clf, X, y, **kwargs):
        from sklearn.metrics import roc_auc_score

        # Generate predictions
        if hasattr(clf, 'decision_function'):
            y_pred = clf.decision_function(X)
        elif hasattr(clf, 'predict_proba'):
            y_pred = clf.predict_proba(X)
        else:
            y_pred = clf.predict(X)

        # score
        classes = set(y)
        if y_pred.ndim == 1:
            y_pred = y_pred[:, np.newaxis]

        _score = list()
        for ii, this_class in enumerate(classes):
            _score.append(roc_auc_score(y == this_class,
                                        y_pred[:, ii]))
            if (ii == 0) and (len(classes) == 2):
                _score[0] = 1. - _score[0]
                break
        return np.mean(_score, axis=0)
