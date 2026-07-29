---
title: Changes to Sample Data in Spartacus 6.0
---


<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; Jekyll directives and links were normalized. See docs/SOURCE.json and docs/UPSTREAM_LICENSE.txt in the skill root. -->
## Checkout Library

The following changes were made to the checkout library sample data in Spartacus 6.0.

The `CheckoutReviewOrderComponent` was replaced by the following CMS components:

- `CheckoutReviewPaymentComponent`
- `CheckoutReviewOverviewComponent`
- `CheckoutReviewShippingComponent`
- `CheckoutReviewPickupComponent`

## Order Library

The following changes were made to the order library sample data in Spartacus 6.0.

- `OrderConfirmationOverviewComponent` and `OrderConfirmationItemsComponent` were removed.
- `OrderConfirmationPickUpComponent` and `OrderConfirmationBillingComponent` were added.
- `AccountOrderDetailsOverviewComponent` was replaced by `AccountOrderDetailsSimpleOverviewComponent`.
- `AccountOrderDetailsItemsComponent` was replaced by `AccountOrderDetailsGroupedItemsComponent`.
- `AccountOrderDetailsBillingComponent` was added.
