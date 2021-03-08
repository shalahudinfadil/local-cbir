import sqlite3
import os

class DB:

    def __init__(self, db = 'cbir.db'):
        self.db = db
        self.connection = sqlite3.connect(self.db)

        self.init_database()
    
    def init_database(self):
        with self.connection as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS folderpath (id INTEGERY PRIMARY KEY, folderpath TEXT, vptreepath TEXT, imagenumber INTEGER)')
            conn.execute('CREATE TABLE IF NOT EXISTS hash (id INTEGERY PRIMARY KEY, hash TEXT, folderpath_id INTEGER, is_serialised INTEGER DEFAULT 0, FOREIGN KEY(folderpath_id) REFERENCES folderpath(id))')
            conn.execute('CREATE TABLE IF NOT EXISTS filepath (id INTEGERY PRIMARY KEY, filepath TEXT, hash_id INTEGER, FOREIGN KEY(hash_id) REFERENCES hash(id))')

    def insert_index(self, folderpath, hashes, treepath, imageNumber):
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO folderpath (folderpath, vptreepath, imagenumber) values (?,?,?)',(folderpath,treepath, imageNumber))
        folderpathLastId =  cursor.lastrowid
        
        for h in hashes:
            cursor.execute('INSERT INTO hash(hash, folderpath_id) VALUES (?,?)',(str(h), folderpathLastId))
            hashLastId = cursor.lastrowid
            for filepath in hashes[h]:
                cursor.execute('INSERT INTO filepath (filepath, hash_id) VALUES (?,?)',(filepath, hashLastId))
        
        self.connection.commit()
    
    def get_folder_index(self, folderpath=None):
        cursor = self.connection.cursor()
        if folderpath is None:
            cursor.execute('SELECT * FROM folderpath')
        else:
            sql = 'SELECT * FROM folderpath WHERE folderpath IN (%s)' % ','.join('?'*len(folderpath))
            cursor.execute(sql, tuple(folderpath))
        result = cursor.fetchall()

        return result
    
    def get_hashes_images(self, hashList):
        cursor = self.connection.cursor()
        sql = 'SELECT h.rowid, h.hash, h.folderpath_id, f.filepath FROM hash h JOIN filepath f ON h.rowid = f.hash_id WHERE h.hash IN (%s)' % ','.join('?'*len(hashList))
        print(sql)
        cursor.execute(sql, tuple(hashList))

        return cursor.fetchall()
    
    def delete_folders_data(self, folderlist):
        cursor = self.connection.cursor()

        sqlSelectFolders = 'SELECT rowid,vptreepath FROM folderpath WHERE folderpath IN ({})'.format(','.join('?'* len(folderlist)))
        cursor.execute(sqlSelectFolders, tuple(folderlist))
        folderResult = cursor.fetchall()
        
        folderIds = []
        folderTrees = []

        for fRes in folderResult:
            folderIds.append(fRes[0])
            if os.path.exists(fRes[1]):
                os.remove(fRes[1])

        sqlSelectHashes = 'SELECT rowid FROM hash WHERE folderpath_id IN ({})'.format(','.join('?' * len(folderIds)))
        cursor.execute(sqlSelectHashes, tuple(folderIds))
        hashResult = [ i[0] for i in cursor.fetchall()]

        sqlDeletes = [
            ('DELETE FROM filepath WHERE hash_id IN ({})'.format(','.join('?' * len(hashResult))), tuple(hashResult)),
            ('DELETE FROM hash WHERE folderpath_id IN ({})'.format(','.join('?' * len(folderIds))), tuple(folderIds)),
            ('DELETE FROM folderpath WHERE folderpath IN ({})'.format(','.join('?' * len(folderlist))), tuple(folderlist))
        ]
        
        for sql in sqlDeletes:
            cursor.execute(sql[0], sql[1])

        self.connection.commit()

if __name__ == '__main__':
    db = DB()
    