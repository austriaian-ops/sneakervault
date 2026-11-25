from firebase_config import get_db
from google.cloud import firestore

def main():
    db=get_db()
    samples=[('SV-001','Air Jordan 1 Retro','Jordan','Basketball','9',8995,12),('SV-002','Air Force 1','Nike','Lifestyle','8',5995,20),('SV-003','Forum Low','Adidas','Lifestyle','10',5495,8),('SV-004','550','New Balance','Lifestyle','9',6995,4)]
    for sku,name,brand,category,size,price,stock in samples:
        ref=db.collection('sneakers').document(sku)
        if not ref.get().exists: ref.create(dict(sku=sku,name=name,brand=brand,category=category,size=size,price=price,stock=stock,created_at=firestore.SERVER_TIMESTAMP))
    for i,name in enumerate(['Alex Demo','Chris Demo','Sam Demo'],1):
        ref=db.collection('customers').document(f'DEMO-{i}')
        if not ref.get().exists: ref.create(dict(name=name,email=f'demo{i}@example.com',phone='09000000000',address='Sample address',created_at=firestore.SERVER_TIMESTAMP))
    print('Sample sneakers and customers inserted. Add sales through the website to adjust stock.')
if __name__=='__main__': main()
