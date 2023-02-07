import pickle
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
#from sklearn.ensemble import BaggingClassifier
#from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

df = pd.read_csv("./data/raw/train_processed.csv")
df = df.sample(n=50000)
x = df.iloc[:, :-1]
y = df.iloc[:, -1]

smote = SMOTE(random_state=42)
x, y = smote.fit_resample(x, y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)




#clf = BaggingClassifier(
#    estimator=DecisionTreeClassifier(criterion='gini',
#      max_depth=50,
#      min_samples_split=3
#      ),
#    n_estimators=300,
#    bootstrap_features=True,
#    oob_score=True,
#    max_features=1.0
#    )

clf = LogisticRegression(C=0.04, penalty='l2', solver='saga', max_iter=5000,  random_state=42)

clf.fit(x_train , y_train)
y_pred = clf.predict(x_test)
acc = clf.score(x_test, y_test)
print(acc)

metrics = """
Accuracy: {:10.4f}
![Confusion Matrix](plot.png)
""".format(acc)
with open("metrics.txt", "w") as outfile:
    outfile.write(metrics)
conf_matrix = confusion_matrix(y_test, y_pred)
disp = sns.heatmap(conf_matrix/np.sum(conf_matrix), annot=True, cmap='Blues', fmt='.2%')
plt.savefig("plot.png")

pickle.dump(clf, open('./artifacts/model.pkl', 'wb'))
