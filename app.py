from flask import Flask, jsonify, render_template, request
from google.cloud import firestore
from firebase_config import get_db
from datetime import date
from decimal import Decimal, InvalidOperation
import os
app = Flask(__name__)
FIELDS = {'sneakers':['name','brand','category','size','sku','price','stock'], 'customers':['name','email','phone','address'], 'sales':['sneaker_id','customer_id','quantity','sale_date']}
class Problem(Exception):
    def __init__(self, message, status=400): self.message, self.status = message, status
@app.errorhandler(Problem)
def problem(e): return jsonify(error=e.message), e.status
@app.errorhandler(Exception)
def error(e):
    from werkzeug.exceptions import HTTPException
    if isinstance(e, HTTPException): return jsonify(error=e.description), e.code
    app.logger.exception('Request failed')
    return jsonify(error='Database operation failed. Check Firestore credentials and terminal.'), 500

def validate(kind, data):
    if not isinstance(data, dict): raise Problem('Expected JSON object')
    result = {}
    for field in FIELDS[kind]:
        v = data.get(field)
        if v is None or isinstance(v, (dict,list,bool)) or not str(v).strip(): raise Problem(f'{field} is required')
        if field in ('stock','quantity'):
            try: v = int(str(v))
            except ValueError: raise Problem(f'{field} must be an integer')
            if v < (1 if field=='quantity' else 0): raise Problem(f'Invalid {field}')
        elif field=='price':
            try:
                d=Decimal(str(v))
                if not d.is_finite() or d<=0 or d>100000000: raise ValueError()
                v=float(d.quantize(Decimal('.01')))
                if v<=0: raise ValueError()
            except (InvalidOperation,ValueError): raise Problem('Invalid price')
        else:
            v=str(v).strip()
            if len(v)>500: raise Problem(f'{field} is too long')
            if field=='email' and ('@' not in v or '.' not in v.split('@')[-1]): raise Problem('Invalid email')
            if field=='sale_date':
                try: date.fromisoformat(v)
                except ValueError: raise Problem('Invalid sale date')
            if field.endswith('_id') and '/' in v: raise Problem('Invalid reference')
        result[field]=v
    return result

def row(s): return dict(s.to_dict(), id=s.id)
@app.get('/')
def home(): return render_template('index.html')
@app.get('/api/health')
def health():
    list(get_db().collection('sneakers').limit(1).stream()); return jsonify(connected=True)
@app.route('/api/<kind>', methods=['GET','POST'])
@app.route('/api/<kind>/<rid>', methods=['GET','PUT','DELETE'])
def records(kind,rid=None):
    if kind not in FIELDS: raise Problem('Unknown collection',404)
    db=get_db(); col=db.collection(kind)
    if request.method=='GET':
        if rid:
            s=col.document(rid).get()
            if not s.exists: raise Problem('Record not found',404)
            return jsonify(row(s))
        q=request.args.get('q','').lower().strip()
        return jsonify([row(s) for s in col.stream() if not q or q in str(s.to_dict()).lower()])
    ref=col.document(rid) if rid else col.document()
    deleting=request.method=='DELETE'; creating=request.method=='POST'
    data=None if deleting else validate(kind,request.get_json(silent=True))
    @firestore.transactional
    def change(tx):
        old=ref.get(transaction=tx)
        if not creating and not old.exists: raise Problem('Record not found',404)
        previous=old.to_dict() or {}
        if kind=='sales':
            # Read all documents before writing; restore previous stock on edit/delete.
            ids=set()
            if old.exists: ids.add(previous['sneaker_id'])
            if data: ids.add(data['sneaker_id'])
            refs={i:db.collection('sneakers').document(i) for i in ids}
            docs={i:r.get(transaction=tx) for i,r in refs.items()}
            if any(not s.exists for s in docs.values()): raise Problem('Referenced sneaker not found')
            stocks={i:s.to_dict()['stock'] for i,s in docs.items()}
            if old.exists: stocks[previous['sneaker_id']]+=previous['quantity']
            if data:
                customer=db.collection('customers').document(data['customer_id']).get(transaction=tx)
                if not customer.exists: raise Problem('Customer not found')
                i=data['sneaker_id']; stocks[i]-=data['quantity']
                if stocks[i]<0: raise Problem('Insufficient stock',409)
                price=previous['unit_price'] if old.exists and previous['sneaker_id']==i else docs[i].to_dict()['price']
                data.update(unit_price=price,total=round(price*data['quantity'],2),sneaker_name=docs[i].to_dict()['name'],customer_name=customer.to_dict()['name'])
            for i,r in refs.items(): tx.update(r,{'stock':stocks[i]})
        elif deleting:
            field='sneaker_id' if kind=='sneakers' else 'customer_id'
            if list(db.collection('sales').where(filter=firestore.FieldFilter(field,'==',ref.id)).limit(1).stream(transaction=tx)):
                raise Problem('Delete related sales first',409)
        if deleting: tx.delete(ref)
        elif creating: tx.create(ref,dict(data,created_at=firestore.SERVER_TIMESTAMP))
        else: tx.update(ref,data)
    change(db.transaction())
    if deleting: return jsonify(message='Deleted successfully')
    return jsonify(row(ref.get())),201 if creating else 200
if __name__=='__main__': app.run(host='127.0.0.1',port=int(os.getenv('PORT','5000')),debug=False)
