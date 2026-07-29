---
title: Escape Focus
---


<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; Jekyll directives and links were normalized. See docs/SOURCE.json and docs/UPSTREAM_LICENSE.txt in the skill root. -->
> **Note:** This feature is introduced with version 2.0 of the Spartacus libraries.

The `cxFocus` directive provides a feature to focus the host element when the `ESC` key is captured. This is useful for dialogs, as well as for larger parts of the UI that should trap the focus.

When the `ESC` key is captured while the element is already focused, the event is let go, and will "bubble up" to the ancestor tree (this is how browsers treat certain UI events).

Spartacus uses the escape focus for the so-called "skip links", for dialogs (such as modals), and for element groups that must be unlocked initially (for example, a facet).

Whenever the escape focus is handled, an output (`esc`) is emitted, so that additional logic can be applied if needed.

### Configuration

The escape focus only happens if it is configured. The following is an example of configuring the escape focus:

```html
<div [cxFocus]="{ focusOnEscape: true }"></div>
```

The `focusOnDoubleEscape` property can be used to force an auto focus in the case of a recurring escape key.
