import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
from sklearn import metrics

class Model(object):

	def __init__(self, data):
		X, y = self._transform_data(data)

		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=50)
		
		print('Train Data Shape:',self.X_train.shape)
		print('Train Labels Shape:',self.y_train.shape)

	def init_rf(self):
		self.rf = RandomForestClassifier(n_estimators=100)

	def fit_data(self):
		self.rf.fit(self.X_train, self.y_train)

		score = self.rf.score(self.X_test, self.y_test)

		predictions = self.rf.predict(self.X_test)

		print('Accuracy:',score)

		return score, predictions

	def plot_confusion_matrix(self, score, predictions):
		# Plot overall accuracy and accuracy of each individual label
		cm = metrics.confusion_matrix(self.y_test, predictions)
		plt.figure(figsize=(11,11))
		sns.heatmap(cm, annot=True, fmt=".0f", linewidths=.5, square = True);
		plt.ylabel('Actual label');
		plt.xlabel('Predicted label');
		all_sample_title = 'Random Forest Accuracy Score: {0}'.format(score)
		plt.title(all_sample_title, size = 15);
		plt.show()

	def predict(self, data):
		X, y = self._transform_data(data)
		
		predictions = self.rf.predict(X)
		score = self.rf.score(X, y)
		
	def _transform_data(self, data):
		train_data = np.array([i[1] for i in data])
		train_labels = np.array([i[2] for i in data])

		vectorizer = CountVectorizer()
		vectorizer.fit(train_data)
		X = vectorizer.transform(train_data)

		y = train_labels

		return X, y