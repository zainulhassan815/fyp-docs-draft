\pagebreak

# Introduction

## Purpose

This project helps organizations find and understand information buried in large collections of documents. Reviewing documents manually, especially resumes, takes too much time and leads to mistakes. Our system automates this work using AI, making it faster and more reliable.

The system is built to handle document search and resume screening, with room to expand into other areas like general document management.

## Project Scope

Most businesses struggle to manage and make sense of large document collections. This system solves that problem by automating document review and providing tools to search, understand, and analyze documents.

### Key Capabilities

**Document Processing**

The system processes these file types:

- PDF files
- Microsoft Word documents
- Scanned images

**Text Extraction (OCR)**

For scanned or image-based documents, the system extracts readable text. It then:

- Classifies documents by type
- Tags them with relevant metadata
- Converts them into vector embeddings for search

**Natural Language Interface**

- Search documents using plain English queries
- Ask questions about document content

**Retrieval-Augmented Generation (RAG)**

- Finds relevant document content based on the user's query
- Uses semantic search with vector embeddings
- Gives the AI model factual context from stored documents
- Generates responses grounded in source data
- Helps reduce incorrect or irrelevant answers
- Supports question answering for HR and document analysis tasks

### HR Resume Screening

- Helps HR staff screen resumes and shortlist candidates
- Collects resume attachments from incoming emails
- Handles multiple resume formats
- Extracts candidate information:
  - Skills
  - Education
  - Work experience
  - Contact details
- Matches and ranks candidates against:
  - Job descriptions
  - Required skills and experience
- Reduces:
  - Manual screening effort
  - HR workload and processing time

### Benefits

- Reduces manual document processing
- Helps minimize errors in document review and analysis
- Saves time for HR and other departments

### Objectives

- Simplify repetitive document review and classification tasks
- Use AI to support HR screening and compliance monitoring
- Make organizational knowledge easier to access and manage

### Strategic Alignment

This system uses AI to improve document retrieval and resume screening. It offers a practical approach to document search and analysis that can work with different types of organizational documents. The system handles moderate document volumes and can be extended later to support larger datasets if needed.

### Out of Scope

This release does not include:

- Integration with third-party applicant tracking systems (e.g., Indeed, Greenhouse)
- Processing of video or audio files
- Native mobile apps for iOS and Android (planned for future releases)

## References

The following documents and resources were consulted during the preparation of this SRS:

1. Google Cloud Documentation - Document AI Overview
   <https://cloud.google.com/document-ai>

2. Amazon Web Services - Amazon Textract: Extract Text and Data from Documents
   <https://aws.amazon.com/textract>

3. Microsoft Azure - Form Recognizer Documentation
   <https://azure.microsoft.com/en-us/products/form-recognizer>

4. LangChain Documentation - Building Applications with Retrieval-Augmented Generation (RAG)
   <https://python.langchain.com>

5. Hugging Face - Document AI: Understanding Documents with Transformers
   <https://huggingface.co/blog/document-ai>

6. Hugging Face - Transformers and Large Language Models Documentation
   <https://huggingface.co/docs>

7. PyMuPDF Documentation - Working with PDFs in Python
   <https://pymupdf.readthedocs.io>

8. FAISS - Facebook AI Similarity Search Library
   <https://faiss.ai>

9. Tesseract OCR - Optical Character Recognition Engine
   <https://github.com/tesseract-ocr/tesseract>

10. IEEE Standard 830-1998 - IEEE Recommended Practice for Software Requirements Specification

# Overall Description

## Product Perspective

This is a standalone system built to help organizations process and search documents using AI. It offers semantic search, text extraction, and question answering features.

### System Context

The system works as an independent document processing platform that can connect with existing tools and workflows. It complements existing content management systems by adding AI-based search and analysis features.

### Major System Components

The system is made up of several connected components:

| Component              | Description                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| **Document Ingestion** | Handles file uploads, format validation, and document routing            |
| **Processing Engine**  | Performs OCR, text extraction, classification, and metadata generation   |
| **AI/NLP Module**      | Generates vector embeddings, runs semantic search, and powers RAG        |
| **Vector Database**    | Stores document embeddings for similarity-based retrieval                |
| **HR Module**          | Manages Gmail integration, resume collection, and candidate shortlisting |
| **Backend API**        | Coordinates system operations and handles business logic                 |
| **Frontend Interface** | Web application for user interactions                                    |
| **Security Layer**     | Handles authentication, authorization, and data protection               |

![Figure 1: Architecture Diagram](./src/images/architecture_diagram.png){width=100%}

### External Interfaces

The system connects to Gmail (e.g., HR email accounts) for resume collection in the HR module. Email integration uses OAuth authentication without storing credentials. Future versions may include connections to ERP systems and document management platforms.

### Hardware Platform

The system runs on standard server hardware or cloud instances. Users access it through web browsers without needing to install any software.

## Product Features

The system includes the following features:

### Document Processing and Management

Users can upload PDF, Word documents, and scanned images using drag-and-drop or batch uploads. The system then:

- Extracts text using OCR
- Classifies documents by type (resumes, reports, contracts, letters)
- Generates metadata (document type, date, author, and other attributes)
- Stores everything in a searchable format

A dashboard lets users view, sort, filter, preview, download, and delete documents.

### Search and Retrieval

Users can search using natural language queries instead of exact keywords. The system uses vector embeddings to find documents based on meaning, not just matching words. Users can filter results by document type, date range, or other metadata. Results are ranked by relevance and show matching text with highlights.

### Question Answering System

Using Retrieval-Augmented Generation (RAG), the system answers questions about uploaded documents. Users ask questions in plain language through a chat interface. The system finds relevant content and generates responses based on that content.

**Example queries:**

- "Extract skills from candidate John's resume"
- "Summarize the findings in the Q3 report"
- "What are the key terms in this contract?"

### Resume Screening

HR personnel create job descriptions with required skills, education, experience, and other criteria. The HR module connects to Gmail accounts using OAuth authentication and collects resume attachments from incoming emails. It keeps a history of collected resumes and lets HR personnel send follow-up emails to candidates.

### Integration and Workflows

The API layer allows integration with external applications. For example, resumes received via email can start processing tasks. Results can be shared with HR management systems or reporting tools through API endpoints.

### Privacy and Security

The system includes role-based access control, authentication, activity logging, and audit trails to help protect data and support privacy compliance.

## User Classes and Characteristics

### HR Personnel

HR personnel use the system mainly for resume screening and candidate management. They have moderate technical skills and are familiar with recruitment workflows. They need features for:

- Connecting email accounts
- Defining job descriptions
- Reviewing candidate information
- Managing shortlists
- Exporting candidate data
- Communicating with applicants

HR personnel use the system frequently during recruitment cycles and occasionally at other times. The system should reduce the time spent on manual resume review.

### Email Service

The Email Service is an external system that handles email-based tasks in the HR module. It connects to email accounts using OAuth 2.0 to access and collect incoming resume attachments. It runs in the background and performs predefined tasks, helping to sync resumes and reduce manual effort for HR personnel.

## Operating Environment

### Server Environment

- The system can run on Linux servers (Ubuntu 20.04+, CentOS 8+) or Windows Server 2019+
- Minimum hardware:
  - 16 GB RAM (32 GB recommended)
  - Quad-core processor (eight-core recommended)
  - 500 GB storage (SSD preferred)

### Software Dependencies

- Python 3.9+
- PostgreSQL 13+ (for metadata and user data)
- Vector database for embeddings and semantic search (e.g., FAISS, Weaviate, or Chroma)
- OCR libraries for text extraction
- NLP frameworks for document processing
- Web frameworks for API and frontend
- Docker for deployment

### Client Environment

- Supported browsers: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- JavaScript must be enabled
- Stable internet or intranet connection required
- No plugins or software installation needed
- The interface adapts to different screen sizes (desktop and tablet)

### Network Environment

- Network connectivity required between server components and client devices
- HR module needs outbound HTTPS connections to Gmail servers
- Can be deployed behind firewalls with appropriate port configurations
- Client-server communication uses HTTPS

### Integration Environment

- Gmail integration via OAuth 2.0 for HR resume collection
- Future integrations may include document management systems, ERP platforms, or other applications via REST APIs

## Design and Implementation Constraints

### Privacy and Security Constraints

- The system should implement security measures to protect sensitive information
- Data encryption should be applied at rest and in transit
- Audit trails should be maintained for data access and processing activities
- Role-based access control (RBAC) should restrict functionality based on user privileges
- Data storage and processing should comply with relevant data protection regulations (e.g., GDPR, CCPA) based on deployment location

### Technology and Tool Constraints

- The system should use modular components to reduce vendor lock-in
- AI models should be deployable on cloud or local infrastructure based on needs
- The system should support both CPU-only and GPU-accelerated deployments

### Performance Constraints

| Metric                 | Requirement                                      |
| ---------------------- | ------------------------------------------------ |
| OCR Processing         | Complete within 30 seconds per standard document |
| Search Queries         | Return results within 2 seconds                  |
| RAG Question Answering | Generate responses within 10 seconds             |
| Concurrent Users       | Handle multiple users without major slowdowns    |
| Document Capacity      | Support at least 100,000 documents               |

### Interface Constraints

- Gmail integration should use OAuth 2.0 and follow Gmail API usage policies and rate limits
- The web interface should work without special software or browser plugins
- The system should show clear error messages when processing fails

### Regulatory and Policy Constraints

- Organizations deploying the system are responsible for having rights to process uploaded documents
- The system should keep different users' data separate and enforce access controls
- AI-generated content should be clearly identified

## User Documentation

The system will include the following documentation:

### Installation and Deployment Guide

- Can be deployed on Linux or Windows servers using Docker or manual installation
- Requires standard hardware; GPU optional for faster AI processing
- Uses open-source components for backend, frontend, OCR, and AI
- Includes a relational database for metadata and a vector database for search
- Supports OCR, RAG for question answering, email-based resume collection, and role-based access control

### HR Module User Guide

Documentation for HR personnel covering:

- Gmail account connection and resume collection
- Creating and managing job descriptions and screening criteria
- Reviewing extracted candidate information and shortlisting
- Exporting candidate data
- Workflow examples and best practices

### API Documentation

Technical documentation for developers including:

- API endpoint descriptions with supported operations and parameters
- Request and response formats with data structures
- Authentication and authorization requirements
- Error codes and handling procedures
- Generated using Swagger/OpenAPI with usage examples

### Quick Start Guide

A short reference guide for new users covering:

- Common tasks: document upload, search, and question answering
- Step-by-step instructions
- Print-friendly format for use as a reference card

### Video Tutorials

Short instructional videos covering:

- Document upload, search, question answering, and HR module setup
- Available within the system or as downloads
- Supports user training and onboarding

### Release Notes

Documentation for each version including:

- New features, enhancements, and resolved issues
- Known issues and limitations
- Upgrade and deployment instructions where applicable

## Assumptions and Dependencies

### Technical Assumptions

- Hardware has sufficient CPU, memory, and storage
- GPU is optional; the system works on CPU-only machines
- Stable network connection available between system components
- Internet connectivity available for HR module email integration
- Python runtime and libraries remain compatible throughout development

### AI and NLP Model Assumptions

- Language and embedding models are available for local deployment
- OCR provides acceptable accuracy for standard printed documents
- Document quality affects extraction accuracy, especially for scanned or handwritten files
- RAG returns relevant answers for most queries

### Organizational Assumptions

- Organizations provide administrative support for setup and maintenance
- Users have basic computer and web application skills
- Backup and recovery procedures are handled by the deploying organization
- HR departments define clear job requirements for candidate evaluation

### Dependencies

- Python and its ecosystem remain available and maintained
- OCR, NLP, and vector storage libraries remain compatible
- Web frameworks and containerization tools available for deployment
- HR module requires Gmail API access and OAuth 2.0
- Access to test documents and datasets for development
- Academic supervision and feedback for progress
- Trained personnel and documentation for long-term maintenance

# System Features

## User Authentication and Access Control

### Description

This feature provides user authentication and role-based access control so that only authorized users can access features appropriate to their roles.

### Actors

- HR Personnel

### Functional Requirements

**REQ-3.1.1: User Login**

The system shall allow users to log in using email and password.

_Use Case Reference: UC-1 – Login_

**REQ-3.1.2: Password Reset**

The system shall allow users to reset their password using a verification mechanism.

_Use Case Reference: UC-2 – Reset Password_

**REQ-3.1.3: Access Restriction**

The system shall restrict access to features unless the user is authenticated.

_Use Case Reference: UC-1 – Login_

## Document Upload and Processing

### Description

This feature allows HR personnel to upload documents and process them for analysis.

### Actors

- HR Personnel

### Functional Requirements

**REQ-3.2.1: Document Upload**

The system shall allow HR personnel to upload files such as resumes and HR documents.

_Use Case Reference: UC-3 – Upload Files_

**REQ-3.2.2: Text Extraction**

The system shall extract text from uploaded documents using OCR when needed.

_Use Case Reference: UC-4 – Process Document_

**REQ-3.2.3: Document Storage**

The system shall store uploaded documents along with extracted text for retrieval.

_Use Case Reference: UC-3 – Upload Files_

## Search Document

### Description

This feature allows users to search documents and refine results using filters.

### Actors

- HR Personnel

### Functional Requirements

**REQ-3.3.1: Document Search**

The system shall allow users to search documents using keywords or natural language queries.

_Use Case Reference: UC-5 – Search_

**REQ-3.3.2: Search Criteria**

The system shall allow users to search based on criteria such as skills, job role, or date.

_Use Case Reference: UC-5 – Search_

**REQ-3.3.3: Result Ranking**

The system shall display search results ranked by relevance.

_Use Case Reference: UC-5 – Search_

## Filter Document

### Description

This feature allows HR personnel to filter documents based on various criteria.

### Actors

- HR Personnel

### Functional Requirements

**REQ-3.4.1: Document Filter**

The system shall allow users to filter documents based on criteria such as skills, job role, or date.

_Use Case Reference: UC-6 – Filter Document_

## Job Creation and Management

### Description

This feature allows HR personnel to create and manage job postings for resume screening.

### Actors

- HR Personnel

### Functional Requirements

**REQ-3.5.1: Job Description Creation**

The system shall allow HR personnel to create job descriptions with required criteria.

_Use Case Reference: UC-7 – Create Job_

**REQ-3.5.2: Job Posting Editing**

The system shall allow HR personnel to edit existing job postings.

_Use Case Reference: UC-8 – Edit Job_

## Resume Viewing and Candidate Screening

### Description

This feature allows HR personnel to review resumes and shortlist candidates.

### Actors

- HR Personnel

### Functional Requirements

**REQ-3.6.1: View Resume**

The system shall allow HR personnel to view and read extracted resume content.

_Use Case Reference: UC-10 – View Resume_

**REQ-3.6.2: Shortlist Candidate**

The system shall allow HR personnel to shortlist candidates based on job relevance.

_Use Case Reference: UC-11 – Shortlist Candidate_

**REQ-3.6.3: Reject Candidate**

The system shall allow HR personnel to reject candidates.

_Use Case Reference: UC-12 – Reject Candidate_

**REQ-3.6.4: Export to Excel**

The system shall allow HR personnel to export shortlisted candidates to Excel format.

_Use Case Reference: UC-13 – Export Excel_

## Email Integration and Resume Synchronization

### Description

This feature connects the system with email services to collect resumes.

### Actors

- HR Personnel
- Email Service

### Functional Requirements

**REQ-3.7.1: Connect Email**

The system shall allow HR personnel to connect their email account.

_Use Case Reference: UC-14 – Connect Email_

**REQ-3.7.2: Sync Resume from Email**

The system shall sync resume attachments from connected email accounts.

_Use Case Reference: UC-15 – Sync Resume_

## Logs and Metadata Management

### Description

This feature provides visibility into system activities and document data.

### Actors

- HR Personnel

### Functional Requirements

**REQ-3.8.1: View Activity Logs**

The system shall allow users to view activity logs.

_Use Case Reference: UC-17 – View Logs_

**REQ-3.8.2: View Document Metadata**

The system shall allow users to view extracted document metadata such as skills and experience.

_Use Case Reference: UC-18 – View Metadata_

# Use Cases

## UC-01: Login

| Field                        | Description                                                                            |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| **Use Case #**               | UC-01                                                                                  |
| **Context of Use**           | HR personnel logs in to access the system                                              |
| **Scope**                    | User Authentication                                                                    |
| **Primary Actor**            | HR Personnel                                                                           |
| **Stakeholders & Interests** | HR – access to system                                                                  |
| **Pre-Conditions**           | 1. System is running 2. User is registered                                             |
| **Trigger**                  | HR personnel selects Login                                                             |
| **Main Course**              | 1. Open Login Page 2. Enter email and password 3. Validate credentials 4. Grant access |
| **Post-Conditions**          | User redirected to dashboard                                                           |
| **Failure Protection**       | Invalid credentials block access                                                       |
| **Extensions**               | UC-02 Reset Password                                                                   |
| **Open Issues**              | Account lock after multiple failures                                                   |
| **References**               | Use Case Diagram                                                                       |

## UC-02: Reset Password

| Field                        | Description                                           |
| ---------------------------- | ----------------------------------------------------- |
| **Use Case #**               | UC-02                                                 |
| **Context of Use**           | User resets forgotten password                        |
| **Scope**                    | User Authentication                                   |
| **Primary Actor**            | HR Personnel                                          |
| **Stakeholders & Interests** | HR – account recovery                                 |
| **Pre-Conditions**           | User email exists                                     |
| **Trigger**                  | User clicks "Reset Password"                          |
| **Main Course**              | 1. Enter email 2. Verify identity 3. Set new password |
| **Post-Conditions**          | Password updated                                      |
| **Failure Protection**       | Invalid email rejected                                |
| **Extensions**               | Verification timeout                                  |
| **Open Issues**              | Password policy                                       |
| **References**               | Use Case Diagram                                      |

## UC-03: Search Documents

| Field                        | Description                                              |
| ---------------------------- | -------------------------------------------------------- |
| **Use Case #**               | UC-03                                                    |
| **Context of Use**           | HR personnel searches stored documents                   |
| **Scope**                    | Document Retrieval                                       |
| **Primary Actor**            | HR Personnel                                             |
| **Stakeholders & Interests** | HR – document access                                     |
| **Pre-Conditions**           | Documents exist                                          |
| **Trigger**                  | HR personnel enters search query                         |
| **Main Course**              | 1. Enter keywords 2. Search documents 3. Display results |
| **Post-Conditions**          | Matching documents shown                                 |
| **Failure Protection**       | No results handled                                       |
| **Extensions**               | UC-04 Filter Search, UC-05 Export Excel                  |
| **Open Issues**              | Ranking logic                                            |
| **References**               | Use Case Diagram                                         |

## UC-04: Filter Search

| Field                        | Description                         |
| ---------------------------- | ----------------------------------- |
| **Use Case #**               | UC-04                               |
| **Context of Use**           | HR personnel refines search results |
| **Scope**                    | Search Filtering                    |
| **Primary Actor**            | HR Personnel                        |
| **Stakeholders & Interests** | HR – accurate results               |
| **Pre-Conditions**           | Search performed                    |
| **Trigger**                  | HR personnel selects filters        |
| **Main Course**              | 1. Choose filters 2. Apply criteria |
| **Post-Conditions**          | Filtered results displayed          |
| **Failure Protection**       | Invalid filters ignored             |
| **Extensions**               | Multi-filter selection              |
| **Open Issues**              | Filter performance                  |
| **References**               | Use Case Diagram                    |

## UC-05: Export Excel

| Field                        | Description                                    |
| ---------------------------- | ---------------------------------------------- |
| **Use Case #**               | UC-05                                          |
| **Context of Use**           | HR personnel exports search results            |
| **Scope**                    | Data Export                                    |
| **Primary Actor**            | HR Personnel                                   |
| **Stakeholders & Interests** | HR – offline analysis                          |
| **Pre-Conditions**           | Search results available                       |
| **Trigger**                  | HR personnel selects Export                    |
| **Main Course**              | 1. Select export option 2. Generate Excel file |
| **Post-Conditions**          | Excel downloaded                               |
| **Failure Protection**       | Export failure handled                         |
| **Extensions**               | Custom fields                                  |
| **Open Issues**              | File size limits                               |
| **References**               | Use Case Diagram                               |

## UC-06: Create Job

| Field                        | Description                      |
| ---------------------------- | -------------------------------- |
| **Use Case #**               | UC-06                            |
| **Context of Use**           | HR personnel creates job opening |
| **Scope**                    | Job Management                   |
| **Primary Actor**            | HR Personnel                     |
| **Stakeholders & Interests** | HR – job posting                 |
| **Pre-Conditions**           | User logged in                   |
| **Trigger**                  | HR personnel selects Create Job  |
| **Main Course**              | 1. Enter job details 2. Save job |
| **Post-Conditions**          | Job created                      |
| **Failure Protection**       | Invalid data blocked             |
| **Extensions**               | UC-07 Edit/Delete Job            |
| **Open Issues**              | Job template                     |
| **References**               | Use Case Diagram                 |

## UC-07: Edit/Delete Job

| Field                        | Description                          |
| ---------------------------- | ------------------------------------ |
| **Use Case #**               | UC-07                                |
| **Context of Use**           | HR personnel updates job information |
| **Scope**                    | Job Management                       |
| **Primary Actor**            | HR Personnel                         |
| **Stakeholders & Interests** | HR – job accuracy                    |
| **Pre-Conditions**           | Job exists                           |
| **Trigger**                  | HR personnel selects edit/delete     |
| **Main Course**              | 1. Modify Job 2. Save or delete      |
| **Post-Conditions**          | Job updated                          |
| **Failure Protection**       | Unauthorized action blocked          |
| **Extensions**               | Job history                          |
| **Open Issues**              | Audit trail                          |
| **References**               | Use Case Diagram                     |

## UC-08: Receive Email

| Field                        | Description                                              |
| ---------------------------- | -------------------------------------------------------- |
| **Use Case #**               | UC-08                                                    |
| **Context of Use**           | System receives resumes via email                        |
| **Scope**                    | Resume Collection                                        |
| **Primary Actor**            | Email Service                                            |
| **Secondary Actor**          | System                                                   |
| **Stakeholders & Interests** | HR – resume intake                                       |
| **Pre-Conditions**           | Email integration enabled                                |
| **Trigger**                  | Incoming email                                           |
| **Main Course**              | 1. Receive email 2. Extract attachments 3. Store resumes |
| **Post-Conditions**          | Resume added to system                                   |
| **Failure Protection**       | Invalid attachment ignored                               |
| **Extensions**               | Multiple attachments                                     |
| **Open Issues**              | Spam handling                                            |
| **References**               | Use Case Diagram                                         |

## UC-09: Sync Resumes

| Field                        | Description                        |
| ---------------------------- | ---------------------------------- |
| **Use Case #**               | UC-09                              |
| **Context of Use**           | System syncs resumes from email    |
| **Scope**                    | Resume Synchronization             |
| **Primary Actor**            | Email Service                      |
| **Stakeholders & Interests** | HR – updated data                  |
| **Pre-Conditions**           | New emails received                |
| **Trigger**                  | Sync scheduled                     |
| **Main Course**              | 1. Fetch emails 2. Process resumes |
| **Post-Conditions**          | Resumes indexed                    |
| **Failure Protection**       | Duplicate check                    |
| **Extensions**               | Manual sync                        |
| **Open Issues**              | Sync frequency                     |
| **References**               | Use Case Diagram                   |

## UC-10: View Logs

| Field                        | Description                          |
| ---------------------------- | ------------------------------------ |
| **Use Case #**               | UC-10                                |
| **Context of Use**           | HR personnel reviews system activity |
| **Scope**                    | Logging                              |
| **Primary Actor**            | HR Personnel                         |
| **Stakeholders & Interests** | HR – auditing                        |
| **Pre-Conditions**           | Logs exist                           |
| **Trigger**                  | HR personnel selects View Logs       |
| **Main Course**              | 1. Retrieve logs 2. Display entries  |
| **Post-Conditions**          | Logs shown                           |
| **Failure Protection**       | Empty logs handled                   |
| **Extensions**               | Filter logs                          |
| **Open Issues**              | Log retention                        |
| **References**               | Use Case Diagram                     |

## UC-11: View Metadata

| Field                        | Description                          |
| ---------------------------- | ------------------------------------ |
| **Use Case #**               | UC-11                                |
| **Context of Use**           | HR personnel views document metadata |
| **Scope**                    | Metadata Management                  |
| **Primary Actor**            | HR Personnel                         |
| **Stakeholders & Interests** | HR – document insight                |
| **Pre-Conditions**           | Document exists                      |
| **Trigger**                  | HR personnel selects View Metadata   |
| **Main Course**              | 1. Fetch metadata 2. Display info    |
| **Post-Conditions**          | Metadata shown                       |
| **Failure Protection**       | Missing metadata handled             |
| **Extensions**               | Metadata edit                        |
| **Open Issues**              | Standard fields                      |
| **References**               | Use Case Diagram                     |

## UC-12: Read Resumes

| Field                        | Description                       |
| ---------------------------- | --------------------------------- |
| **Use Case #**               | UC-12                             |
| **Context of Use**           | HR personnel reads resume content |
| **Scope**                    | Resume Analysis                   |
| **Primary Actor**            | HR Personnel                      |
| **Stakeholders & Interests** | HR – candidate review             |
| **Pre-Conditions**           | Resume processed                  |
| **Trigger**                  | HR personnel selects resume       |
| **Main Course**              | 1. Load resume 2. Display content |
| **Post-Conditions**          | Resume displayed                  |
| **Failure Protection**       | OCR fallback                      |
| **Extensions**               | Highlight skills                  |
| **Open Issues**              | Formatting                        |
| **References**               | Use Case Diagram                  |

\pagebreak

# Diagrams

## Use Case Diagram

![Figure 2: Use Case Diagram](./src/images/use_case_diagram.png){width=100%}

## Activity Diagram

![Figure 3: Activity Diagram](./src/images/activity_diagram.png){height=8in}

## DFD Diagrams

### Level 0

![Figure 4: DFD Level 0 Diagram](./src/images/dfd_level_0.jpeg){width=100%}

### Level 1

![Figure 5: DFD Level 1 Diagram](./src/images/dfd_level_1.jpeg){width=100%}

### Level 2

![Figure 6: DFD Level 2 Diagram](./src/images/dfd_level_2.png){width=100%}
