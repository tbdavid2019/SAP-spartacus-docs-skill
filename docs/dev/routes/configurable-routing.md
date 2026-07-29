---
title: Configurable Routing
feature:
- name: Configurable Routing
  spa_version: 1.0
  cx_version: n/a
---


<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; Jekyll directives and links were normalized. See docs/SOURCE.json and docs/UPSTREAM_LICENSE.txt in the skill root. -->
In a single-page application, you control what the user sees by showing different views of the app. Spartacus uses the Angular Router to take care of navigating from one view to another. The Router does this by treating each URL as an instruction to present a specific view.

Spartacus allows you to customize these URLs, giving you more control over SEO and storefront usability. Spartacus includes default routes for accessing the different views, which you can use without any configuration. You also have the option to customize any route that you want in Spartacus.

For more information, see the following:

- [Adding and Customizing Routes](adding-and-customizing-routes.md)
- [Route Configuration](route-configuration.md)
- [Configurable Router Links](configurable-router-links.md)
- [Disabling Standard Routes](disabling-standard-routes.md)
- [Route Aliases](route-aliases.md)
- [External Routes](external-routes.md)
- [Early Login](early-login.md)

## Limitations

- Translation of routes in many languages is currently not supported.
- Configuration of lazy-loaded routes is currently not supported.
- Routing based on [Angular's `HashLocationStrategy`](https://angular.io/guide/router#locationstrategy-and-browser-url-styles) is not supported.
- [Secondary routes and named router outlets](https://angular.io/guide/router-tutorial-toh#secondary-routes) are currently not supported.
