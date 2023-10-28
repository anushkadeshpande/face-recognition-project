def compareEmbeddings(classifierModel, embeddings):
    yhat_class = classifierModel.predict(embeddings)
    yhat_prob = classifierModel.predict_proba(embeddings)
    class_index = yhat_class[0]
    class_probability = yhat_prob[0,class_index] * 100

    return class_index, class_probability