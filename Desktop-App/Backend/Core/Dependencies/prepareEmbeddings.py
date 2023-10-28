def PrepareEmbeddings():
    import os

    from facenet_embeddings import facenet_embeddings
    from facenet_embeddings_512 import facenet_512_embeddings
    from vggface_embeddings import vggface_embeddings
    from dlib_resnet_embeddings import dlib_resnet_embeddings
    from arcface_embeddings import arcface_embeddings
    
    if not os.path.exists('Backend/Core/Generations/embeddings'):
        os.makedirs('Backend/Core/Generations/embeddings')
    facenet_embeddings()
    facenet_512_embeddings()
    vggface_embeddings()
    dlib_resnet_embeddings()
    arcface_embeddings()
