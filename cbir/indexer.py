import os
import pickle
import uuid

import vptree
import cv2
from imutils import paths

from db.db import DB
import cbir.hashing as hashing

db = DB()

def indexer(folderpath):
    imagePaths = list(paths.list_images(folderpath))
    imageNumber = len(imagePaths)
    if imageNumber > 0:
        hashes = {}

        for (i, imagePath) in enumerate(imagePaths):
            image = cv2.imread(imagePath)
            h = hashing.dhash(image)
            h = hashing.convert_hash(h)

            l = hashes.get(h, [])
            l.append(imagePath)
            hashes[h] = l
        
        points = list(hashes.keys())
        tree = vptree.VPTree(points, hashing.hamming)

        treepath = os.path.join('tree', str(uuid.uuid4())+'.tree')

        if not os.path.exists('tree'):
            os.mkdir('tree')

        with open(treepath, 'wb') as f:
            f.write(pickle.dumps(tree))

        db.insert_index(folderpath, hashes, treepath, imageNumber)

        return True
    else:
        return False

def check_folder_serialized(folderpath):
    return db.get_folder_index(folderpath)
    

if __name__ == '__main__':
    print(indexer('E:\Python\local-cbir-hashing\image'))