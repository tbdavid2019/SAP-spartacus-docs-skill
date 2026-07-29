---
title: Event Service
feature:
- name: Event Service
  spa_version: 2.0
  cx_version: n/a
- name: Event Type Inheritance
  spa_version: 3.1
  cx_version: n/a
  anchor: "#event-type-inheritance"
---


<!-- Mechanically prepared from SAP/spartacus-docs under Apache-2.0; Jekyll directives and links were normalized. See docs/SOURCE.json and docs/UPSTREAM_LICENSE.txt in the skill root. -->
The Spartacus event service provides a stream of events that you can consume without a tight integration to specific components or modules. The event system is used in Spartacus to build integrations to third party systems, such as tag managers and web trackers.

The event service also allows you to decouple certain components. For example, you might have a component that dispatches an event, and another component that reacts to this event, without requiring any hard dependency between the components.

The event service leverages RxJs Observables to drive the streams of events.

***

**Table of Contents**

- This will become a table of contents (this text will be scrapped).
{:toc}

***

## Event Types

Events are driven by TypeScript classes, which are signatures for a given event and can be instantiated. The following is an example:

```typescript
import { CxEvent } from "@spartacus/core";
export class CartAddEntryEvent extends CxEvent {
  cartId: string;
  userId: string;
  productCode: string;
  quantity: number;
}
```

## Observing Events

To observe events of a given type, you can get the stream for the event type, and then subscribe to it whenever you need. The following is an example for the `CartAddEntryEvent` call:

```typescript
constructor(events: EventService){}
/* ... */

const result$ = this.events.get(CartAddEntrySuccessEvent);
result$.subscribe((event) => console.log(event));
```

## Pulling Additional Data From Facades

If you need more data than what is contained in a particular event, you can combine this data with other streams. For example, you can collect additional data from facades.

The following is an example of reacting to an "added to cart event", followed by waiting for the cart to be stable (because the OCC cart needs to be reloaded from the back end), and then appending all of the cart data to the data from the event:

```typescript
constructor(
    events: EventService,
    cartService: ActiveCartService
    ){}
/* ... */

const result$ = this.events.get(CartAddEntrySuccessEvent).pipe(
    // When the above event is captured, wait for the cart to be stable
    // (because OCC reloads the cart after any cart operation)...
    switchMap((event) =>
        this.cartService.isStable().pipe(filter(Boolean), mapTo(event))
    ),
    // Merge the state snapshot of the cart with the data from the event:
    withLatestFrom(this.cartService.getActive()),
    map(([event, cart]) => ({ ...event, cart }))
);
```

### No Performance Cost for Unused Events

Since the event service leverages RxJs Observables, event streams are lazy. This means that no defined computations happen (such as pulling data from facades) until someone subscribes to the particular stream of events. The following is an example:

```typescript
result$.subscribe((event) => {
  // < log the event (for example, to a tag manager) >
});
```

## Registering Event Sources

In theory, any RxJs Observable can be a source of events as soon as it emits objects of the declared class type. In practice, there are some limitations, as described in [Avoiding Certain Candidates for an Event Stream](#avoiding-certain-candidates-for-an-event-stream), below.

The following is an example of how to register an RxJs `Subject` as a source of events of type `CustomEvent`:

```typescript
const subject$ = new Subject<CustomEvent>();
const unregister = eventService.register(CustomEvent, subject$);
```

**Note:** It is possible to register multiple sources to a single event type, even without knowing it, because multiple decoupled features can attach sources to the same event type. The following is an example:

```typescript
eventService.register(CustomEvent, subject1$);
eventService.register(CustomEvent, subject2$);
```

## Avoiding Certain Candidates for an Event Stream

Not all RxJs Observables are good candidates for an event stream. For example, the NgRx selectors are not good candidates for an event stream. The Observable of the NgRx selector replays the latest updated value at the moment of the subscription, regardless of when the value was updated. But a valid event stream should emit a value only when the actual event happens.

Examples of candidates to avoid for event sources are the following Observables and their derivatives, including Spartacus facades that use the following under the hood:

- NgRx state selectors
- `BehaviorSubject` and `ReplaySubject` from RxJs
- Observables with the piped operators `replay()` and `shareReplay()` from RxJs
- Observables created by the operators `of()` and `from()` from RxJs
- anything that emits a value simply because a subscription was made.

A pure RxJs `Subject` is a good candidate for the event source.

## Avoiding Memory Leaks and Unregistering Event Sources

To avoid memory leaks, every event source Observable should be unregistered from the `EventService` when it is no longer needed. To unregister an event source, you can call the "tear down" function that is returned by the `register()` method. The following is an example:

```typescript
const unregister = eventService.register(CustomEvent, subject$);
/* ... */
unregister(); // Calling the handler assigned from `eventService.register(...)` in the example above
```

**Note:** Completed Observables must be unregistered manually. They will not be unregistered automatically on stream completion.

## Dispatching Individual Events

The `register()` method is intended to register RxJs Observables. However, event instances can also be dispatched individually, using the `dispatch()` method. For example, in your component logic, you could call the following:

```typescript
constructor(events: EventService){}
/* ... */

onClick() {
  this.events.dispatch(new CustomUIEvent(...));
}
```

## Event Type Inheritance

> **Note:** This functionality is introduced with version 3.1 of the Spartacus libraries.

Parent events allow you to group similar events under one common event. The parent event can be an abstract class or a regular class. By subscribing to the parent event, you get emissions from all of the child events that inherit it.

For example, `PageEvent` from `@spartacus/storefrontlib` is a parent event, and all of the child page events, such as `HomePageEvent`, `CartPageEvent`, and `ProductDetailsPageEvent`, inherit from this parent. If you subscribe to `PageEvent`, you will get emissions from all of the child page events that inherit from `PageEvent`. The following is an example:

```typescript
eventService.get(PageEvent).subscribe(...) // receives all page events
```

All events should inherit from the `CxEvent` that is in `@spartacus/core`, as shown in the following example:

```typescript
import { CxEvent } from "@spartacus/core";
export class MyEvent extends CxEvent {...}
```

Although this is not required for events to work properly, if all events inherit from `CxEvent`, it allows you to observe all events at once, as shown in the following example:

```typescript
eventService.get(CxEvent).subscribe(...) // receives all Spartacus events.
```

**Note:** Observing all Spartacus events at once may have significant effects on performance, so it should be done with care.

### Observing Events in Older Versions of Spartacus

If you are using a version of Spartacus that is older than release 3.1, for every event that you wish to observe, you must subscribe to it individually, as shown in the following example:

```typescript
eventService.get(HomePageEvent).subscribe(...), eventService.get(CartPageEvent).subscribe(...), eventService.get(ProductDetailsPageEvent).subscribe(...), eventService.get(CategoryPageResultsEvent).subscribe(...), eventService.get(SearchPageResultsEvent).subscribe(...)
```

## List of Spartacus Events

The following table lists all of the available events in Spartacus, and where to find them in the Spartacus source code.

| Event | File Path |
| --- | --- |
| GetTicketQueryResetEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| GetTicketQueryReloadEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| GetTicketsQueryResetEvents | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| GetTicketsQueryReloadEvents | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| NewMessageEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| TicketReopenedEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| TicketClosedEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| GetTicketCategoryQueryResetEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| GetTicketCategoryQueryReloadEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| GetTicketAssociatedObjectsQueryResetEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| GetTicketAssociatedObjectsQueryReloadEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| TicketCreatedEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| CreateEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| UploadAttachmentSuccessEvent | `feature-libs/customer-ticketing/root/events/customer-ticketing.events.ts` |
| OrderEvent | `feature-libs/order/root/events/order.events.ts` |
| OrderPlacedEvent | `feature-libs/order/root/events/order.events.ts` |
| ReplenishmentOrderScheduledEvent | `feature-libs/order/root/events/order.events.ts` |
| DownloadOrderInvoicesEvent | `feature-libs/order/root/events/order.events.ts` |
| QuoteDetailsReloadQueryEvent | `feature-libs/quote/core/event/quote.events.ts` |
| CdcLoadUserTokenFailEvent | `integration-libs/cdc/root/events/cdc-event.ts` |
| CdcReConsentEvent | `integration-libs/cdc/root/events/cdc-event.ts` |
| HomePageEvent | `projects/storefrontlib/events/home/home-page.events.ts` |
| NavigationEvent | `projects/storefrontlib/events/navigation/navigation.event.ts` |
| PageEvent | `projects/storefrontlib/events/page/page.events.ts` |
| ProductDetailsPageEvent | `projects/storefrontlib/events/product/product-page.events.ts` |
| CategoryPageResultsEvent | `projects/storefrontlib/events/product/product-page.events.ts` |
| SearchPageResultsEvent | `projects/storefrontlib/events/product/product-page.events.ts` |
| CartPageEvent | `feature-libs/cart/base/root/events/cart-page.events.ts` |
| CartEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CreateCartEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CreateCartSuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CreateCartFailEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartAddEntryEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartAddEntrySuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartAddEntryFailEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartRemoveEntryFailEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartRemoveEntrySuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartUpdateEntrySuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartUpdateEntryFailEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| CartUiEventAddToCart | `feature-libs/cart/base/root/events/cart.events.ts` |
| MergeCartSuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| LoadCartEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| RemoveCartEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| DeleteCartEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| DeleteCartSuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| DeleteCartFailEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| AddCartVoucherEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| AddCartVoucherSuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| AddCartVoucherFailEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| RemoveCartVoucherEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| RemoveCartVoucherSuccessEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| RemoveCartVoucherFailEvent | `feature-libs/cart/base/root/events/cart.events.ts` |
| SavedCartEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| SaveCartEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| SaveCartSuccessEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| SaveCartFailEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| RestoreSavedCartEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| RestoreSavedCartSuccessEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| RestoreSavedCartFailEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| EditSavedCartEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| EditSavedCartSuccessEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| EditSavedCartFailEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| CloneSavedCartEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| CloneSavedCartSuccessEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| CloneSavedCartFailEvent | `feature-libs/cart/saved-cart/root/events/saved-cart.events.ts` |
| CheckoutQueryReloadEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutQueryResetEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryAddressEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryAddressCreatedEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryAddressSetEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryAddressClearedEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryModeEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryModeSetEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryModeClearedEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutDeliveryModeClearedErrorEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutSupportedDeliveryModesQueryReloadEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutSupportedDeliveryModesQueryResetEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutPaymentDetailsEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutPaymentDetailsCreatedEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutPaymentDetailsSetEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutPaymentCardTypesQueryReloadEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| CheckoutPaymentCardTypesQueryResetEvent | `feature-libs/checkout/base/root/events/checkout.events.ts` |
| UserAccountEvent | `feature-libs/user/account/root/events/user-account.events.ts` |
| UserAccountChangedEvent | `feature-libs/user/account/root/events/user-account.events.ts` |
| ModuleInitializedEvent | `projects/core/src/lazy-loading/events/module-initialized-event.ts` |
| FacetChangedEvent | `projects/core/src/product/event/product.events.ts` |
| LanguageSetEvent | `projects/core/src/site-context/events/site-context.events.ts` |
| CurrencySetEvent | `projects/core/src/site-context/events/site-context.events.ts` |
| UserAddressEvent | `projects/core/src/user/events/user.events.ts` |
| UpdateUserAddressEvent | `projects/core/src/user/events/user.events.ts` |
| DeleteUserAddressEvent | `projects/core/src/user/events/user.events.ts` |
| AddUserAddressEvent | `projects/core/src/user/events/user.events.ts` |
| LoadUserAddressesEvent | `projects/core/src/user/events/user.events.ts` |
| LoadUserPaymentMethodsEvent | `projects/core/src/user/events/user.events.ts` |
| SearchBoxSuggestionSelectedEvent | `projects/storefrontlib/cms-components/navigation/search-box/search-box.events.ts` |
| SearchBoxProductSelectedEvent | `projects/storefrontlib/cms-components/navigation/search-box/search-box.events.ts` |
| LogoutEvent | `projects/core/src/auth/user-auth/events/user-auth.events.ts` |
| LoginEvent | `projects/core/src/auth/user-auth/events/user-auth.events.ts` |
| ComponentEvent | `projects/storefrontlib/cms-structure/page/component/events/component.event.ts` |
| ComponentCreateEvent | `projects/storefrontlib/cms-structure/page/component/events/component.event.ts` |
| ComponentDestroyEvent | `projects/storefrontlib/cms-structure/page/component/events/component.event.ts` |
