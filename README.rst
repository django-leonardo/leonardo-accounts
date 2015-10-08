
==========================
Leonardo Leonardo Accounts
==========================

Oscar Accounts integration to Leonardo Store (Payment method, Profile Actions, Admin Dashboard). This module uses our fork which works with Oscar 1.0 and Django 1.8. Basically this module support managing user accounting on your Django Site. This is just wrapper around standard ``accounts`` app with auto load to Leonardo CMS.

For leonardo use ``pip install -e git+https://github.com/michaelkuty/django-oscar-accounts#egg=accounts``

.. contents::
    :local:

Features
--------

* An account has a credit limit which defaults to zero. Accounts can be set up with no credit limit so that they are a 'source' of money within the system. At least one account must be set up without a credit limit in order for money to move around the system.

* Accounts can have:

	* No users assigned
	* A single "primary" user - this is the most common case
	* A set of users assigned
	* A user can have multiple accounts

* An account can have a start and end date to allow its usage in a limited time window

* An account can be restricted so that it can only be used to pay for a range of products.

* Accounts can be categorised

* integration to Leonardo Store (Payment method, Profile Actions, Admin Dashboard)

Installation
------------

.. code-block:: bash

    pip install leonardo_accounts

Read More
=========

* https://github.com/django-leonardo/django-leonardo
* https://github.com/django-oscar/django-oscar-accounts
* https://github.com/michaelkuty/django-oscar-accounts
