---
title: Keyboard Focus
feature:
- name: Keyboard Focus
  spa_version: 2.0
  cx_version: n/a
---


<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; Jekyll directives and links were normalized. See docs/SOURCE.json and docs/UPSTREAM_LICENSE.txt in the skill root. -->
> **Note:** This feature is introduced with version 2.0 of the Spartacus libraries.

The `cxFocus` directive handles keyboard-specific features in Spartacus related to focus management. These features are essential for keyboard-only users.

The keyboard features are used for a host element, and for the focusable elements of the inner DOM of the host element. Focusable elements are HTML elements that receive focus when you use the keyboard. For example, by tabbing through the experience, focusable elements are highlighted and provide access to key features, such as "open product", "add to cart", and so on.

There are many keyboard focus features. While most of these features work in isolation, there is often a correlation between them. This is why all features are handled by a single `cxFocus` directive. The directive ensures that the features do not conflict, and that they work well together.

The various features of the `cxFocus` directive are documented separately, as follows:

| Feature | Description |
| --- | --- |
| [Visible Focus](visible-focus.md) | Limits the visible focus to keyboard users only. |
| [Persist Focus](persist-focus.md) | Refocuses an element based on its last focus state. |
| [Escape Focus](escape-focus.md) | Traps the focus of an element when the user presses the `ESC` key. |
| [Auto Focus](auto-focus.md) | Provides auto focus in a single-page experience. |
| [Trap Focus](trap-focus.md) | Traps the focus of a group of focusable elements, so that focus returns to the first element after leaving the last element. |
| [Lock Focus](lock-focus.md) | Locks and unlocks the focus of the focusable child elements of the host element. |

All features have separate configuration typings, but all configurations are accessible through the `FocusConfig`.

The various features can be used with a single directive. The following is an example:

```html
<div
  [cxFocus]="{
    autofocus: 'input[submit:true]',
    lock: true,
    trap: true }"
></div>
```
