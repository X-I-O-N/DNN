from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier
import pickle
import sklearn
from sklearn import *
import os
os.environ["CUDA_VISIBLE_DEVICES"]="1,2,3"  
import numpy
import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from gplearn.genetic import SymbolicRegressor
from mlxtend.classifier import StackingClassifier
from mlxtend.regressor import StackingRegressor
import sklearn.linear_model as lm
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load dataset
dataframe = pandas.read_csv("L-all-blip-else-trainingset.csv", header=None)
dataset = dataframe.values
# split into input (X) and output (Y) variables
#X = dataset[:,0:1288].astype(float)
X = dataset[:,0:1288]
y = dataset[:,1288]

# encode class values as integers
#encoder = LabelEncoder()
#encoder.fit(Y)
#encoded_Y = encoder.transform(Y)

# baseline model
def create_baseline():
	# create model
	model = Sequential()
	model.add(Dense(1288, input_dim=1288, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model


# larger model
def create_larger():
	# create model
	model = Sequential()
	model.add(Dense(1288, input_dim=1288, kernel_initializer='normal', activation='relu'))
	model.add(Dense(644, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# smaller model
def create_smaller():
	# create model
	model = Sequential()
	model.add(Dense(644, input_dim=1288, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# define wider model
def wider_model():
	# create model
	model = Sequential()
	model.add(Dense(644, input_dim=1288, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
	return model

modelname = "keras"
if modelname == "keras":
	estimators = []
	estimators.append(('standardize', StandardScaler()))
	estimators.append(('mlp', KerasClassifier(build_fn=create_smaller, epochs=100, batch_size=5, verbose=0)))
	models = Pipeline(estimators)
if modelname == "gp":
	models = SymbolicRegressor(population_size=5000,
                           generations=2, stopping_criteria=0.01,
                           p_crossover=0.7, p_subtree_mutation=0.1,
                           p_hoist_mutation=0.05, p_point_mutation=0.1,
                           max_samples=0.9, verbose=1,
                           parsimony_coefficient=0.01, random_state=0)
if modelname == "DNNGPBLEND":
	estimators = []
	estimators.append(('standardize', StandardScaler()))
	estimators.append(('mlp', KerasRegressor(build_fn=wider_model, epochs=100, batch_size=5, verbose=0)))
	DNN = Pipeline(estimators)
	est_gp = SymbolicRegressor(population_size=5000,
                           generations=20, stopping_criteria=0.01,
                           p_crossover=0.7, p_subtree_mutation=0.1,
                           p_hoist_mutation=0.05, p_point_mutation=0.1,
                           max_samples=0.9, verbose=1,
                           parsimony_coefficient=0.01, random_state=0)
	lr = lm.LogisticRegression()
 	#gbc = sklearn.ensemble.GradientBoostingClassifier()
	models = [StackingRegressor(regressors=[DNN,est_gp], meta_regressor=lr)]

if modelname == "DTGPBLEND":
	clf1 = sklearn.tree.DecisionTreeRegressor(max_depth=4)
	est_gp = SymbolicRegressor(population_size=5000,
                           generations=20, stopping_criteria=0.01,
                           p_crossover=0.7, p_subtree_mutation=0.1,
                           p_hoist_mutation=0.05, p_point_mutation=0.1,
                           max_samples=0.9, verbose=1,
                           parsimony_coefficient=0.01, random_state=0)
	lr = lm.LogisticRegression()
 	#gbc = sklearn.ensemble.GradientBoostingClassifier()
	models = [StackingRegressor(regressors=[clf1,est_gp], meta_regressor=lr)]

if modelname == "DNNTEST":
	scale = StandardScaler()
	X = scale.fit_transform(X)
	Y = scale.fit_transform(Y)
	DNN = KerasRegressor(build_fn=create_smaller, epochs=1, batch_size=5, verbose=0)
	est_gp = sklearn.tree.DecisionTreeClassifier(max_depth=4)
	#lr = lm.LogisticRegression()
 	#gbc = sklearn.ensemble.GradientBoostingClassifier()
	models = [sklearn.ensemble.VotingClassifier(estimators=[('DNN1', DNN), ('DNN2', est_gp)], voting='soft', weights=[1, 1])]

# BEST IS 133
model_ridge = lm.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=9081)
model_randomforest = RandomForestClassifier(n_estimators = 200)
model_lasso = lm.LogisticRegression(penalty = "l1", C = 9081)
model_gbt = GradientBoostingClassifier(n_estimators = 200)

pred_ridge = []
pred_randomforest = []
pred_lasso = []
pred_gbt = []
new_Y = []
for i in range(10):
    indxs = np.arange(i, X.shape[0], 10)
    indxs_to_fit = list(set(range(X.shape[0])) - set(np.arange(i, X.shape[0], 10)))
    pred_ridge = pred_ridge + list(model_ridge.fit(X[indxs_to_fit[:]], y[indxs_to_fit[:]]).predict_proba(X[indxs,:])[:,1])
    pred_randomforest = pred_randomforest + list(model_randomforest.fit(X[indxs_to_fit[:]], y[indxs_to_fit[:]]).predict_proba(X[indxs,:])[:,1])
    pred_lasso = pred_lasso + list(model_lasso.fit(X[indxs_to_fit[:]], y[indxs_to_fit[:]]).predict_proba(X[indxs,:])[:,1])
    pred_gbt = pred_gbt + list(model_gbt.fit(X[indxs_to_fit[:]], y[indxs_to_fit[:]]).predict_proba(X[indxs,:])[:,1])
    new_Y = new_Y + list(y[indxs[:]])
	
                                                                   
new_X = np.hstack((np.array(pred_ridge).reshape(len(pred_ridge), 1), np.array(pred_randomforest).reshape(len(pred_randomforest), 1), np.array(pred_lasso).reshape(len(pred_lasso), 1), np.array(pred_gbt).reshape(len(pred_gbt), 1)))
print new_X
new_Y = np.array(new_Y).reshape(len(new_Y), 1)

# <codecell>

#model_stacker = lm.LogisticRegression()
model_stacker = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)
print np.mean(cross_val_score(model_stacker, new_X, new_Y.reshape(new_Y.shape[0]), cv=5))

model_stacker.fit(new_X, new_Y.reshape(new_Y.shape[0]))
#save model to disk
filename = 'blendedmodel.sav'
pickle.dump(model_stacker, open(filename, 'wb'))
print "all done Teerth"

importances = model_stacker.feature_importances_
std = np.std([tree.feature_importances_ for tree in model_stacker.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

#print (model_stacker.coef_)
#print (model_stacker.feature_importances_)
# Plot the feature importances of the forest
#plt.figure()
#plt.title("Feature importances")
#plt.bar(range(X.shape[1]), importances[indices],
       #color="r", yerr=std[indices], align="center")
#plt.xticks(range(X.shape[1]), indices)
#plt.xlim([-1, X.shape[1]])
#plt.show()
#models.fit(X, Y)
#score = models.score(X, Y)

#print('Done. Score:', score)
#kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
#results = cross_val_score(models, X, encoded_Y, cv=kfold)
#results = cross_val_score(models, X, Y, cv=kfold)
#print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
#print("Wider: %.2f (%.2f) MSE" % (results.mean(), results.std()))
