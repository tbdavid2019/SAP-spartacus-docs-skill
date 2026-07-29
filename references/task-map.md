# SAP Spartacus Task Map

Use this map when the core lookup table in `SKILL.md` does not cover the task. Read only the relevant group, then locate exact pages through `docs/SKILL_INDEX.md` or `rg`.

## Installation and Upgrade

| Task | Documentation |
| --- | --- |
| Development prerequisites | `docs/install/recommended-development-environment.md` |
| Frontend installation | `docs/install/frontend/` |
| Backend installation | `docs/install/backend/` |
| Schematics and feature selection | `docs/install/schematics.md` |
| Feature flags | `docs/install/configuring-feature-flags.md` |
| Version migration | `docs/home/updating-to-version-*` |
| Breaking changes | `docs/contributing/breaking-changes.md` |

## Architecture and Backend Communication

| Task | Documentation |
| --- | --- |
| Architecture overview | `docs/dev/architecture.md` |
| OCC/custom backend communication | `docs/dev/backend_communication/` |
| Commands and queries | `docs/dev/commands-and-queries.md` |
| Global configuration | `docs/dev/global-configuration-in-spartacus.md` |
| State management and persistence | `docs/dev/state_management/` |
| Type augmentation | `docs/dev/type-augmentation.md` |

## UI, CMS, Routing, and Styling

| Task | Documentation |
| --- | --- |
| Components | `docs/dev/components/` |
| CMS component customization | `docs/dev/components/customizing-cms-components.md` |
| Outlets | `docs/dev/outlets.md` |
| Routing | `docs/dev/routes/` |
| Styling and page layout | `docs/dev/styling-and-page-layout/` |
| Internationalization | `docs/dev/i18n.md` |
| SmartEdit | `docs/install/smartEdit-setup-instructions-for-spartacus.md` and `docs/dev/smartedit-contract.md` |

## Runtime Quality

| Task | Documentation |
| --- | --- |
| SSR | `docs/dev/ssr/` |
| Performance and Core Web Vitals | `docs/dev/performance/` |
| PWA | `docs/dev/pwa/` |
| SEO | `docs/dev/seo/` |
| Accessibility | `docs/dev/accessibility/` |
| Security | `docs/dev/security/` |
| HTTP errors | `docs/dev/http-error-handling.md` |

## Commerce Features and Integrations

| Task | Documentation |
| --- | --- |
| Cart, checkout, ASM, coupons, orders | `docs/dev/features/` |
| Third-party integrations | `docs/install/integrations/` |
| B2B organization | `docs/dev/features/b2b-commerce-organization.md` and `docs/using/commerceorg/` |
| Financial Services Accelerator | `docs/fsa/` |
| Telco and Utilities Accelerator | `docs/telco/` |

## Search Patterns

Search by both product vocabulary and implementation symbol:

```bash
rg -n -i "oauth|authorization code|resource owner" docs/dev
rg -n -i "cmscomponent|componentwrapper|outlet" docs/dev
rg -n -i "ssr|rendering|timeout|transferstate" docs/dev
rg -n -i "221121|2211-jdk21|migration" docs/home docs/dev
rg -n -i "exact error text or class name" docs
```

For a production error, also search the HTTP status, endpoint fragment, configuration key, feature toggle, and visible error text separately.
