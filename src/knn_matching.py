from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load

def train_knn_model(X, k, save_path=''):
    
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(X)
    dump(knn_model, save_path)
    return knn_model


def predict_cluster(input_data,model_path=''):
    model=load(model_path)
    return model.predict([input_data])