# DKBOTZDB

**Welcome to DKBOTZDB**! 🚀

**DkBotzDB Is The Most Powerful And Developer-Friendly Database Solution Powered By DKBotz And DkBotzPro, Offering Fast, Reliable, Scalable, And Secure Data Management. Designed For Effortless Integration And Built With Modern API Standards, DkBotzDB Ensures Smooth Performance Across Applications, Backed By The Trust And Excellence of [dkbotzpro.in](https://db.dkbotzpro.in).**

---

## Features

- **Fast and Reliable Database Interaction**: Easily insert, find, update, and delete records.
- **Smart Find**: Advanced query capabilities with options for sorting, limiting, and skipping results.
- **API Driven**: Powered by HTTP requests, making it easy to integrate with any system.
- **Scalable**: Handle large data volumes without compromising performance.
- **Secure**: Supports secure API communication.

---

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Available Methods](#available-methods)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [How to Suggest a New Feature](#how-to-suggest-a-new-feature)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

You can install `DKBOTZDB` by cloning this repository and manually installing the required dependencies.

### 1. Clone the repository:
```bash
git clone https://github.com/DKBotz/DKBOTZDB.git
```

### 2. Install the required Python libraries:
You need the following dependencies:
- `requests`: To make HTTP requests.
- `colorlog`: For colored logging output.

Run this command to install the necessary dependencies:
```bash
pip install -r requirements.txt
```

### 3. Create `requirements.txt`:
```txt
requests
colorlog
```

---

## Setup

1. Create an account on [DKBotzPro](https://db.dkbotzpro.in).
2. Obtain your **API Token** from the DKBotzPro dashboard.
3. Choose or create a **collection** where you want to store data.

---

## Usage

Here is how you can integrate `DKBOTZDB` into your Python projects.

### Basic Example:
```python
from dkbotzdb import DkBotzDB

# Initialize and set token and collection
db = DkBotzDB()['YOUR_TOKEN']['your_collection']

# Add data to the collection
db.insert_one({"name": "Amit", "age": 25})

# Retrieve a record
result = db.find_one({"name": "Amit"})
print(result)

# Update a record
db.update_one({"name": "Amit"}, {"$set": {"age": 26}})

# Delete a record
db.delete_one({"name": "Amit"})

# Count documents in the collection
count = db.count_documents()
print(f"Total documents: {count}")
```

---

## Available Methods

`DkBotzDB` supports various methods for interacting with your database:

### 1. **insert_one(data)**

Adds a single record to the collection.

- **Parameters**: `data` (dict): The data to be inserted.
- **Returns**: The result of the insert operation (if successful).

### 2. **find(query)**

Finds records based on the provided query.

- **Parameters**: `query` (dict): The query criteria.
- **Returns**: List of matching records.

### 3. **find_one(query)**

Finds the first matching record based on the provided query.

- **Parameters**: `query` (dict): The query criteria.
- **Returns**: The first matching record or `None`.

### 4. **smart_find(query, limit=None, skip=None, sort=None)**

Finds multiple records with advanced filtering options.

- **Parameters**:
  - `query` (dict): The query criteria.
  - `limit` (int): Limit the number of results (optional).
  - `skip` (int): Skip a certain number of records (optional).
  - `sort` (dict): Sorting criteria (optional).
- **Returns**: List of matching records.

### 5. **update_one(query, update_data)**

Updates a single record.

- **Parameters**:
  - `query` (dict): The query to find the document.
  - `update_data` (dict): The data to update.
- **Returns**: The result of the update operation.

### 6. **deletemany(query)**

Deletes multiple records based on the query.

- **Parameters**: `query` (dict): The query to delete matching records.
- **Returns**: The result of the deletion.

### 7. **delete_one(query)**

Deletes a single record based on the query.

- **Parameters**: `query` (dict): The query to delete the record.
- **Returns**: The result of the deletion.

### 8. **count_documents(query={})**

Counts the number of documents matching the query.

- **Parameters**: `query` (dict, optional): The query criteria (default is an empty query).
- **Returns**: The number of matching documents.

---

## Logging

`DKBOTZDB` uses **colored logging** to provide real-time feedback in the terminal. Each log level is color-coded for easy identification:

- `DEBUG`: Cyan
- `INFO`: Green
- `WARNING`: Yellow
- `ERROR`: Red
- `CRITICAL`: Bold Red

You can change the logging level by modifying the `logger.setLevel()` in the code.

---

## How to Suggest a New Feature

At **DKBOTZDB**, we’re always eager to improve and enhance the database solution by adding new features that make it even more powerful and user-friendly. If you have an idea for a new feature, we'd love to hear from you! 🚀

1. **Search for Existing Feature Requests**: Before submitting a new feature suggestion, please check the existing [GitHub Issues](https://github.com/DKBOTZPROJECT/DKBOTZDB/issues) to see if your idea has already been suggested. This helps us avoid duplicates and keep everything organized.

2. **Create a New Issue**:
   - If your feature hasn’t been suggested already, you can submit a **new issue**. To do this, go to our [GitHub Issues page](https://github.com/DKBOTZPROJECT/DKBOTZDB/issues), click on the **"New Issue"** button, and select **"Feature Request"**.
   - Provide a **clear and detailed description** of the feature you'd like to suggest.
   - Mention the **use cases** where this feature would be helpful and how it can improve the user experience.

3. **Be Specific and Provide Examples**:
   - The more details you provide, the easier it will be for us to understand and consider your suggestion.
   - You can include code snippets, user stories, or any relevant links that will help us understand your request.
   
4. **Stay Engaged**: 
   - After submitting your feature suggestion, be available to answer any questions or provide more information if necessary.
   - If we need clarification or additional details, we’ll comment on your issue.

### Example of a Good Feature Request:
   - **Title**: "Add ability to update multiple records at once"
   - **Description**: "Currently, the `update_one()` function is available, but it would be really helpful if we could update multiple records at once. This could be beneficial for bulk operations like updating multiple users' status at the same time."
   - **Use Case**: "I have a situation where I need to update the status of multiple records based on certain criteria. It would save time and resources to do this in a single API call."

We appreciate all suggestions and contributions from our community, and we will review each feature request carefully. Together, we can continue making **DKBOTZDB** better!

You can submit your suggestions here: [GitHub Issues](https://github.com/DKBOTZPROJECT/DKBOTZDB/issues).

## Contributing

We welcome contributions to improve `DKBOTZDB`. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Support

For any issues, feel free to raise a GitHub issue or contact us at dkbotzpro@gmail.com.

---

