Bromine is a high-level web testing library based on [Selenium][1] and [PageObject Pattern][2].

It's purpose is to provide a conceptual framework to **model** the system under test.  
To write actual tests you'll keep using your testing framework of choice.

Bromine focuses on **end-to-end tests**: it relies on [Selenium][1] to exercise a
*real* system, not to simulate it.

While Selenium serves as the essential foundation enabling end-to-end testing,  
WebDriver alone offers too low a level of abstraction.
When we *describe* some behaviour that our system must exhibit, we usually think  
about how users interact with the UI and how this one is expected to respond to
those interactions. We do *not* think about the browser as the main actor, but
indeed as part of the application. In the context of Object-Oriented Programming,
as developers we tend to reason in terms of UI objects interacting with the user
or with other parts of the system.  
Given this perspective shift, Bromine adopts [PageObject Pattern][2] as its other pillar.

The three basic building blocks of Bromine's conceptual model are `WebApplication`,
`WebPage` and `WebElement`.

`WebElements` are responsible for locating and automatically refreshing themselves in
order to relieve the programmer of the burden of explicitly handling Selenium's
[StaleElementExceptions][3].


[1]: https://www.seleniumhq.org/
[2]: https://martinfowler.com/bliki/PageObject.html
[3]: https://docs.seleniumhq.org/exceptions/stale_element_reference.jsp
