# SneakerVault — Sneaker Inventory and Sales Management System

## Project Overview

SneakerVault is a web-based sneaker inventory and sales management system developed using Python Flask and Firebase Cloud Firestore. It provides a centralized platform for managing sneaker collections, customer information, inventory stocks, sales transactions, and sales reports.

The system features a modern streetwear-inspired interface designed to provide an interactive, responsive, and user-friendly experience.

## Live Website

**Vercel Deployment:** https://sneakervault-nine.vercel.app/

## Project Objectives

- Provide centralized management of sneaker inventory.
- Maintain organized customer information.
- Monitor available sneaker stocks.
- Manage and record sales transactions.
- Automatically update inventory quantities.
- Implement CRUD operations using Firebase Cloud Firestore.
- Maintain accurate records through data validation.

## Technologies Used

- Python Flask
- HTML5
- CSS3
- JavaScript
- Firebase Cloud Firestore
- Firebase Admin SDK
- Python-dotenv
- PyCharm
- GitHub
- Vercel

## System Features

- Interactive dashboard
- Sneaker inventory management
- Customer information management
- Sales transaction management
- Automatic stock adjustment
- Create, Read, Update, and Delete (CRUD) operations
- Search functionality
- Individual record viewing
- Data validation
- Sales reports
- Responsive website interface
- Dark and light theme

## Database Collections

| Collection | Description |
|---|---|
| sneakers | Stores sneaker information, sizes, SKUs, and inventory records. |
| customers | Stores customer information. |
| sales | Stores sales transactions with sneaker and customer references. |

## Database Operations

- Creating, updating, and deleting sales automatically adjusts inventory stocks through Firestore transactions.
- Deleting a sale reverses its corresponding stock movement.
- Sneakers and customers associated with existing sales cannot be deleted.
- Sales reports display totals based on saved Firestore records.

## Installation and Setup

1. Open the SneakerVault project in PyCharm.
2. Create and activate a Python virtual environment.
3. Install the required dependencies using `python -m pip install -r requirements.txt`.
4. Create a Firebase project and enable Cloud Firestore.
5. Download the Firebase service account credentials.
6. Save the credentials locally as `ServiceAccountKey.json`.
7. Configure the `.env` file using `.env.example`.
8. Publish the provided `firestore.rules` in the Firebase Console.
9. Optionally, run `python seed_data.py` to insert sample sneaker and customer records.
10. Run `python app.py` to start the application.

**Local Website:** http://127.0.0.1:5000/

**Database Connectivity Test:** http://127.0.0.1:5000/api/health

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Check database connectivity |
| GET | /api/{collection} | Retrieve records |
| POST | /api/{collection} | Create a record |
| GET | /api/{collection}/{id} | Retrieve a specific record |
| PUT | /api/{collection}/{id} | Update a record |
| DELETE | /api/{collection}/{id} | Delete a record |

## Vercel Deployment

SneakerVault is configured for cloud deployment using Vercel and Firebase Cloud Firestore.

Firebase credentials are configured securely through the `FIREBASE_SERVICE_ACCOUNT` environment variable.

## Security and Data Privacy

- Firebase service account credentials must not be uploaded to GitHub.
- Environment variables must remain confidential.
- The Firebase Admin SDK uses server-side authorization.
- This application is intended for classroom demonstration using fictional records.
- Authentication and access controls are required before public production use.

## Academic Purpose

This project was developed as part of the Advanced Database Final Practical Activity to demonstrate database management, CRUD operations, cloud database integration, and web application deployment.

## Submission Requirements

- Private GitHub repository
- Complete project source code
- README.md documentation
- Firebase Cloud Firestore integration
- Instructor collaborator: `kidlat14`

---

**SneakerVault — Collect. Manage. Sell.**

Developed for educational purposes.
