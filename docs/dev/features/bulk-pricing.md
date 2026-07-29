---
title: Bulk Pricing
feature:
  - name: Bulk Pricing
    spa_version: 3.2
    cx_version: 2005
---


<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; Jekyll directives and links were normalized. See docs/SOURCE.json and docs/UPSTREAM_LICENSE.txt in the skill root. -->
> **Note:** This feature is introduced with version 3.2 of the Spartacus libraries.

Bulk Pricing allows users to see potential savings for specific products when they are purchased in bulk. A pricing table is displayed on the product details page that lists the different price tiers for the product, based on the quantity that is purchased.

## Enabling Bulk Pricing

You can enable bulk pricing by selecting it as an option when installing the `@spartacus/product` feature library. For more information, see [Installing Additional Spartacus Libraries](https://sap.github.io/spartacus-docs/schematics/#installing-additional-spartacus-libraries).

Bulk Pricing is driven by CMS. You can add the bulk pricing table to your product pages using ImpEx similar to the following:

```text
$contentCatalog=powertools-spaContentCatalog
$contentCV=catalogVersion(CatalogVersion.catalog(Catalog.id[default=$contentCatalog]),CatalogVersion.version[default=Online])[default=$contentCatalog:Online]

INSERT_UPDATE ContentSlot;$contentCV[unique=true];uid[unique=true];name;cmsComponents(uid, $contentCV)
;;ProductSummarySlot;Summary for product details;ProductImagesComponent,ProductIntroComponent,ProductSummaryComponent,VariantSelector,BulkPricingTableComponent,AddToCart,ConfigureProductComponent

INSERT_UPDATE CMSFlexComponent;$contentCV[unique=true];uid[unique=true];name;flexType
;;BulkPricingTableComponent;BulkPricingTableComponent;BulkPricingTableComponent
```

## Configuring

No special configuration is required.

## Extending

No special extensibility is available for this feature.
