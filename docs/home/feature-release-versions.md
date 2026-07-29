---
title: Feature Compatibility
---


<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; Jekyll directives and links were normalized. See docs/SOURCE.json and docs/UPSTREAM_LICENSE.txt in the skill root. -->
The following table lists the Spartacus libraries release version for each feature, as well as the relevant version of SAP Commerce Cloud that is required.

Spartacus is compatible with SAP Commerce Cloud version 1905 or higher, although SAP Commerce Cloud version 2005 or newer is recommended. In the table below, you can see which Spartacus features require API endpoints that are only available in newer versions of SAP Commerce Cloud.

**Note:** For the required version of SAP Commerce Cloud, some features do not rely on specific endpoints in the back end, so the version indicated in the table is `n/a` (that is, not applicable).

**Note:** For versions that are indicated with an asterisk (*), see the relevant feature documentation for further details.

| Feature | Spartacus Version | Commerce Cloud Version |
| --- | ---: | ---: |
| [Above-the-Fold Loading](../dev/performance/above-the-fold.md) | 1.4 | n/a |
| [Anonymous Consent](../dev/features/anonymous-consent.md) | 1.3 | 1905 |
| [Applied Promotions](../dev/features/applied-promotions.md) | 2.0 | 1905 |
| [Assisted Service Module](../dev/features/asm.md) | 1.3 | 1905 |
| [Auth Config Initializer](../dev/features/auth-config-initializer.md) | 221121.15.0 | 2211-jdk21.1 |
| [Authentication](../dev/authentication.md) | 221121.1.0 | 2211-jdk21.0 |
| [Automatic Multi-Site Configuration](../dev/context/automatic-context-configuration.md) | 1.3 | 1905 |
| [Automatic Theme Configuration](../dev/context/automatic-context-configuration.md#automatic-theme-configuration) | 3.2 | 1905 |
| [B2B Commerce Organization](../dev/features/b2b-commerce-organization.md) | 3.0 | 2005 |
| [B2B Organization User Registration](../dev/features/b2b-organization-user-registration.md) | 6.0 | 2205 |
| [Banner Component](../dev/components/banner-component.md) | 1.0 | n/a |
| [Bulk Pricing](../dev/features/bulk-pricing.md) | 3.2 | 2005 |
| [Cancellations and Returns](../dev/features/cancellations-and-returns.md) | 1.4 | 2005 |
| [Carousel Component](../dev/components/carousel-component.md) | 1.0 | n/a |
| [Cart Import and Export](../dev/features/cart-import-export.md) | 4.2 | 2011 |
| [Cart Validation](../dev/features/cart-validation.md) | 4.2 | 2011 |
| [Clear Cart](../dev/features/clear-cart.md) | 5.0 | 1905 |
| [Commands and Queries](../dev/commands-and-queries.md) | 3.2 | n/a |
| [Configurable Products Integration](../install/integrations/configurable-products-integration.md) | 3.1 | 2005 |
| [Configurable Routing](../dev/routes/configurable-routing.md) | 1.0 | n/a |
| [Consignment Tracking](../dev/features/consignment-tracking.md) | 1.2 | 1905 |
| [Coupons](../dev/features/coupons.md) | 1.3 | 1905 |
| [CPQ Configurable Products Integration](../install/integrations/cpq-configurable-products-integration.md) | 3.3 | 2005 |
| [Customer Coupons](../dev/features/customer-coupons.md) | 1.5 | 1905 |
| [Customer Data Cloud Integration](../install/integrations/cdc-integration.md) | 3.2 | n/a |
| [Customer Interests](../dev/features/customer-interests.md) | 1.4 | 1905 |
| [Deferred Loading](../dev/performance/deferred-loading.md) | 1.4 | n/a |
| [DEPRECATED - SAP Enterprise Product Development Visualization Integration](../install/integrations/epd-visualization-integration.md) | 4.3 | 2105 |
| [Directionality](../dev/styling-and-page-layout/directionality.md) | 2.1 | 1905 |
| [Early Login](../dev/routes/early-login.md) | 1.2 | n/a |
| [Event Service](../dev/features/event-service.md) | 2.0 | n/a |
| [Event Type Inheritance](../dev/features/event-service.md#event-type-inheritance) | 3.1 | n/a |
| [Express Checkout](../dev/features/express-checkout.md) | 1.2 | n/a |
| [Extending Built-In Models](../dev/type-augmentation.md) | 2.1 | 1905 |
| [External Routes](../dev/routes/external-routes.md) | 1.2 | n/a |
| [Feature Flags](../install/configuring-feature-flags.md) | 1.1 | n/a |
| [Federated Login](../dev/features/federated-login.md) | 221121.11.0 | 2211-jdk21.11 |
| [Future Stock](../dev/features/future-stock.md) | 6.0 | 2205 |
| [Global Messages](../dev/global-messages.md) | 1.0 | n/a |
| [Guest Checkout](../dev/features/guest-checkout.md) | 1.2 | 1905 |
| [HTML Tags](../dev/seo/html-tags.md) | 1.0 | n/a |
| [Image Lazy Loading](../dev/components/shared-components/media-component.md#image-lazy-loading) | 3.0 | n/a |
| [Image Zoom](../dev/features/image-zoom.md) | 4.2 | 2011 |
| [Infinite Scroll](../dev/features/infinite-scroll.md) | 1.2 | n/a |
| [Intelligent Selling Services for SAP Commerce Cloud Integration](../install/integrations/cds-integration.md) | 1.5 | 1905.9 |
| [Inventory Display](../dev/features/inventory-display.md) | 4.1 | 2005 |
| [Keyboard Accessibility](../dev/accessibility/best-practices/keyboard-accessibility.md) | 2.0 | n/a |
| [Keyboard Focus](../dev/accessibility/keyboard-focus/keyboard-focus.md) | 2.0 | n/a |
| [Lazy Loading of CMS components](../dev/lazy-loading-guide.md#lazy-loading-of-cms-components) | 2.0 | n/a |
| [Lazy Loading of Modules](../dev/lazy-loading-guide.md#lazy-loading-of-modules) | 2.1 | n/a |
| [Loader Meta Reducer](../dev/state_management/loader-meta-reducer.md) | 1.0 | n/a |
| [Loading Scopes](../dev/backend_communication/loading-scopes.md) | 1.4 | n/a |
| [Media Component](../dev/components/shared-components/media-component.md) | 2.0 | n/a |
| [multi-dimensional-products](../dev/features/product-multi-dimensional.md) | 2211.28 | 2211.28 |
| [Notification Preferences](../dev/features/notification-preferences.md) | 1.4 | 1905 |
| [Open Payment Framework Integration](../install/integrations/open-payment-framework-integration-deprecated.md) | [NOT_SPECIFIED_YET] | 2211 |
| [Pagination Component](../dev/components/shared-components/pagination.md) | 2.0 | n/a |
| [Password Visibility Component](../dev/components/shared-components/password-visibility-component.md) | 5.0 | n/a |
| [Popover Component](../dev/components/shared-components/popover-component.md) | 3.2 | n/a |
| [Proxy Facades](../dev/proxy-facades.md) | 3.2 | n/a |
| [PWA](../dev/pwa/pwa-home.md) | 1.0 | n/a |
| [Qualtrics Integration](../install/integrations/qualtrics-integration.md) | 1.3 | n/a |
| [Quick Order](../dev/features/quick-order.md) | 4.1 | 2011 |
| [Santorini Theme](../dev/styling-and-page-layout/storefront-themes.md) | 4.0 | n/a |
| [SAP Digital Payments Integration](../install/integrations/digital-payments-integration.md) | 4.1 | 2011* or 2105* |
| [Saved Cart](../dev/features/saved-cart.md) | 3.2 | 2005 |
| [Scheduled Replenishment](../dev/features/scheduled-replenishment.md) | 3.0 | 2005 |
| [Scroll Position Restoration](../dev/features/scroll-position-restoration.md) | 4.2 | n/a |
| [Scroll to Top](../dev/features/scroll-to-top.md) | 5.0 | n/a |
| [Searchbox Component](../dev/components/searchbox-component.md) | 1.0 | n/a |
| [Selective Cart](../dev/features/selective-cart.md) | 1.5 | 1905 |
| [SEO](../dev/seo/seo.md) | 1.0 | n/a |
| [Server-Side Rendering Error Handling](../dev/ssr/server-side-rendering-error-handling.md) | 2211.29 | n/a |
| [Server-Side Rendering Optimization](../dev/ssr/server-side-rendering-optimization.md) | 3.0 | n/a |
| [Session Management](../dev/session-management.md) | 3.0 | 1905 |
| [Site Theming and Site Theme Switcher](../dev/styling-and-page-layout/site-theme.md) | 2211.29 | 2211.29 |
| [Skeleton Design](../dev/styling-and-page-layout/skeleton-design.md) | 3.0 | n/a |
| [Skip Links](../dev/features/skip-links.md) | 1.5 | n/a |
| [SmartEdit for Spartacus](../install/smartEdit-setup-instructions-for-spartacus.md) | 1.0 | 1905 |
| [Split View Component](../dev/components/shared-components/split-view.md) | 3.0 | n/a |
| [Stacked Outlets](../dev/outlets.md#stacked-outlets) | 1.4 | n/a |
| [Standardized SSR Logging](../dev/ssr/server-side-rendering-contextual-logging.md) | 6.2 | n/a |
| [State Persistence](../dev/state_management/state-persistence.md) | 2.0 | n/a |
| [Stock Notification](../dev/features/stock-notification.md) | 1.4 | 1905 |
| [Store Locator](../dev/features/store-locator.md) | 1.2 | 1905 |
| [Structured Data](../dev/seo/structured-data.md) | 1.3 | n/a |
| [Style Versioning](../dev/styling-and-page-layout/css-architecture.md#style-versioning) | 2.0 | n/a |
| [Table Component](../dev/components/shared-components/table-component.md) | 3.0 | n/a |
| [Tag Management System](../dev/features/tag-management-system.md) | 3.2 | n/a |
| [Text Field Configurator Template](../dev/features/text-field-configurator-template.md) | 3.1 | 2005 |
| [Token Revocation](../dev/security/token-revocation.md) | 1.4 | 1905.6 |
| [Variants](../dev/features/variants.md) | 1.5 | 1905 |
| [Wish List](../dev/features/wish-list.md) | 1.4 | 1905 |
