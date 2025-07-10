==========================
Frequently Asked Questions
==========================

This section contains answers to frequently asked questions about the unofficial Tabdeal API.

Why sell orders do not use all of the available balance?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When the order is SELL, Tabdeal doesn't allow all of the borrow-able amount to be used,
This is actually usable when the order is BUY, but on SELL, for unknown reasons, it isn't.
Based on my observations, Tabdeal holds 0.68% to 0.77% of the borrow-able amount,
so we have to reduce the order volume by an amount to make sure it's acceptable.
I chose to reduce the order volume by 1% to be on the safe side.
