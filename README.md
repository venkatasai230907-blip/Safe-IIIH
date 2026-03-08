# SafeCampus - Anonymous Grievance Reporting System

## Problem Statement

Gender Grievance Cells play a crucial role in ensuring safety and inclusivity on campus, yet many students hesitate to report grievances due to lack of awareness, fear of exposure, and inefficient reporting mechanisms. Currently, there is no centralized, user-friendly digital platform that enables secure, anonymous, and transparent reporting of gender-related grievances at IIIT Hyderabad. This gap results in underreporting of incidents and delays in redressal, negatively affecting campus well-being. There is a need for a reliable digital solution that improves accessibility, trust, and efficiency in handling gender-based grievances.

## Solution Approach

SafeCampus is a web-based anonymous grievance reporting system designed to provide a secure and user-friendly platform for students to report gender-related grievances. The application is divided into two main components: a student-facing reporting portal and a password-protected admin dashboard for the committee.

Students can submit reports anonymously, with the option to upload evidence. Upon submission, they receive a unique case key, which they can use to track the status of their report and communicate with the committee through an anonymous chat interface.

The committee can log in to a secure dashboard to view, manage, and respond to the reports. They can update the status of each case, and the changes are reflected in real-time for the student.

## Tech Stack

*   **Backend:** Flask (Python)
*   **Frontend:** HTML, Tailwind CSS, JavaScript
*   **Database:** SQLAlchemy (with SQLite)

## Key Features

*   **Anonymous Reporting:** Students can report grievances without revealing their identity.
*   **Secure Communication:** A two-way anonymous chat allows for secure communication between the student and the committee.
*   **Evidence Upload:** Students can optionally upload files (images, documents, etc.) as evidence.
*   **Case Tracking:** Students can track the status of their report using a unique case key.
*   **Admin Dashboard:** A password-protected dashboard for the committee to manage and respond to reports.
*   **Emergency Button:** A panic button to alert the committee in case of an emergency.
*   **Customizable Categories:** The grievance categories can be easily customized.

## Instructions to Run the Code

1.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```bash
    python app.py
    ```
3.  Open your browser and navigate to `http://127.0.0.1:5001/`.

## Admin Credentials

*   **Username:** user@gmail.com
*   **Password:** user1234

*   **Username:** user2@gmail.com
*   **Password:** user2345

*   **Username:** user3@gmail.com
*   **Password:** user3456

## File Structure

```
.
├── app.py
├── instance
│   └── database.db
├── static
│   └── uploads
├── templates
│   ├── committee.html
│   ├── dashboard.html
│   ├── emergency_numbers.html
│   └── index.html
├── .gitignore
└── README.md
```

## Previous Work

This project was built from scratch.

## AI Disclosure

AI USED: GEMINI PRO
