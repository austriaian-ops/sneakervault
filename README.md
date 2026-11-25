# SneakerVault
Local classroom Flask + Firestore CRUD application. Python 3.11+ recommended.
1. Open this folder in PyCharm. Create/activate a virtual environment.
2. Run `python -m pip install -r requirements.txt`.
3. Create a Firebase project and a Cloud Firestore database. Download a service account JSON from Project settings > Service accounts. Save as ServiceAccountKey.json in this folder. Copy .env.example to .env if missing.
4. Publish firestore.rules in the Firebase console. The Admin SDK uses IAM and bypasses client rules. Never expose the service account or deploy this unauthenticated classroom app publicly.
5. Optional: `python seed_data.py` inserts sample sneakers and customers without overwriting existing sample IDs. Create sample sales in the interface.
6. Run `python app.py` and open http://127.0.0.1:5000. Check /api/health for connectivity.
Collections: sneakers (one document per size/SKU), customers, sales (references both). Sales create/edit/delete adjust stock transactionally. Deleting a referenced sneaker/customer is blocked. Deleting a sale reverses its stock movement. Reports show totals for all saved sales.
API: GET/POST /api/{collection}; GET/PUT/DELETE /api/{collection}/{id}; GET supports q search. Keep .env and service credentials out of Git. Submit private repository with README and invite instructor kidlat14.
