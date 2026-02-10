# Lime CRM Mini Sandbox - Application Consultant Demo

Hi,

My name is Dania and this is a tiny Lime-inspired CRM sandbox that I built to explore the kind of work an Application Consultant Trainee does at Lime.

The focus is not on building a full CRM system, but on showing how I think about:

- data structures for companies, contacts and activities
- simple trigger logic around follow-ups
- making it easy to map information and explain what is going on to a customer

Everything runs locally in a small SQLite database and is intentionally transparent so it is easy to extend, criticise or turn into something more advanced.

## What the demo does

The script behaves like a very small, text based Lime CRM playground:

1. **Companies**

   - Add companies with name, segment and city.
   - This maps to a simple `company` table with an auto-increment id.

2. **Contacts**

   - Add contacts and link them to a company.
   - This maps to a `contact` table with a foreign key to `company`.
   - Each contact can have a role and email, like "CRM owner" or "COO".

3. **Activities**

   - Log activities for a contact: call, meeting, email or task.
   - Store a short summary, creation time and optional follow-up date.
   - A simple trigger sets the initial status:
     - `follow-up scheduled` if a follow-up date is added.
     - otherwise `open`.

4. **Simple trigger rule: follow-up needed**

   When you view the activity board, the script:

   - checks all activities with a due date in the past and status `follow-up scheduled`
   - surfaces them as `follow-up needed` in the overview

   This is a very light-weight version of the kind of automations you describe in the role:
   turning user actions and dates into clear, prioritised next steps.

5. **Activity overview**

   - Shows a small "board" of activities grouped by status and date.
   - Makes it easy to talk about how a customer team would work with the data:
     who to call, which follow-ups are late, etc.

## How it relates to Lime and the trainee role

From your description, an Application Consultant at Lime:

- creates mappings of data structures between objects
- codes automatic triggers based on user actions
- works with SQL and integrations
- explains solutions to customers in a clear way

In this demo I tried to mirror that in a very small, concrete way:

- `company`, `contact` and `activity` show the data structures and relationships.
- SQLite is used as a simple SQL database.
- the follow-up rule is an example of a trigger that turns dates into actions.
- the menu and wording are designed so it is easy to walk through this with a non-technical user.

I would be happy to talk through what I would improve next (for example: adding a REST API, a small web UI, or import/export mappings) if given the chance.

## How to run

1. Make sure you have Python 3.8 or later installed.

2. Open a terminal in this folder and (optionally) create a virtual environment:

   ```bash
   python -m venv .venv
   # On macOS / Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

3. Install dependencies (only the Python standard library is used, but this keeps the workflow familiar):

   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:

   ```bash
   python main.py
   ```

5. Use the menu:

   - `1` - Add company
   - `2` - Add contact
   - `3` - Add activity (with simple trigger logic)
   - `4` - View activity board
   - `5` - Exit

6. A SQLite file called `lime_demo.db` will be created in the same folder. You can inspect it with any SQLite viewer if you want to see the tables directly.

## Files

- `main.py` - main script, menu, database schema and trigger logic.
- `lime_demo.db` - created automatically after first run.
- `requirements.txt` - included for completeness, but only standard library modules are used.

---

Thank you for taking the time to look at this.

Best regards,  
Dania