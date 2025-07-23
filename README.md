# Tallis-Ledger
A concise ledger based accounting system for small charities.

![Screenshot]("./Screenshot.png")

You will need the following software installed on your computer :

```
python
git
sqlite tools
DB Browser (or an alternative such as DBeaver)
```

Once you have installed git you can clone the repository by entering :

```
git clone https://github.com/bjmcgill/Tallis-Ledger
```

This will create a directory called Tallis-Ledger in your current directory. Now type :

```
cd Tallis-Ledger
python -m venv venv
```

This will create a virtual environment into which you can install the necessary libraries. Now on Windows PCs type:

```
venv\Scripts\activate
```

or on a macOS or Linux computer type :

```
source venv/bin/activate
```

Now to install the necessary libraries on a Windows, macOS or Linux computer type :

```
pip install -r requirements.txt
```

You just need to create the tables now by typing :

```
sqlite3 your_ledger.db < createtables.sql
```

You can insert sample data now by typing :

```
sqlite3 your_ledger.db < insertdata.sql
```

Or if you wish to enter data into your own Account and Fund tables use DB Browser. DB Browser is also useful for creating your own reports by entering SQL Select Queries. 

To start the application type :

```
python main.py
```

This program gives users the power and flexibility of double entry bookkeeping without the hassle of complicated accounting software like Sage and Gnucash. On opening the application (and selecting a valid database), you are met with a simple ledger window which you can filter on fund or account. There are three modes: Initial - Where you can add or select a transaction; Add - Where you can add a transaction; and Edit - Where you can select and edit a previous transaction.

Each transaction consists of two or more splits. The sum of all split amounts in a transaction will sum to zero. That is the double entry feature.

The Add and Edit modes give you the capability to cancel, save a transaction, add a split, delete a split, balance a split or delete a transaction.

Suppose you received a £100 from the council as a restricted grant. You would create a restricted income fund called "Council Fund", a "Council Income" account, and you would put the money in the Bank.

You would create the following rows in the Fund and Account tables using DB Browser

**Fund**

| Id | Name | Type |
|:---|:-----|:-----|
| 100 | Council Fund | Restricted Fund |

**Accounts**

| Id | Name | Type |
|:---|:-----|:-----|
| 100 | Bank | Current Asset |
| 200 | Council Income | Restricted Income |

Then you would enter the following double entry in the main ledger window

**Ledger**

| UserDate | Description | FundChoice | AccountChoice | Amount |
|:---------|:------------|:-----------|---------------|--------|
| 2025-07-22 | Grant from Council | Council Fund | Bank | 100 |
| 2025-07-22 | Grant from Council | No Fund | Council Income | -100 |

Note that the second split (row) in the ledger is negative. Money is coming from the income account and going into the bank account. The income is always negative because it is a credit, and the current asset is always positive because it is a debit. This is not what you might expect from looking at a bank statement, but bookkeepers always do it this way.

Once the Accounts and Fund have been entered into the tables using DB Browser, you will be able to select them in the ledger by means of a drop down box.

If you are still confused, I will write more extensive documentation for the application in this repository's wiki.

Thankyou for choosing Tallis Ledger.

BJ McGill 22-07-2025
