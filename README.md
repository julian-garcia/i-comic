# i-Comic
Django based web app to enable registered users to define custom comic strips, request new features and report bugs. Also includes a user forum for general discussion, productivity charts to indicate developer work rates and finally  documentation for developers who wish to contribute.

## Technical approach
The app was developed using web framework **Django** alongside **Python**, using its Model-View-Template structure. Productivity charts are visualised using JavaScript libraries **Chartist.js** and **moment.js**. Dynamic front end elements were implemented using **jQuery**. For device responsiveness **Bootstrap** is employed.

## Features
- _Custom Comic Strip_: Users can define their own personal comic strips by adding self authored images and narrative
- _Tickets_: Raise requests for new features or raise bugs. Upvote to speed up the development of a solution and comment on individual tickets
- _Forum_: Users can raise their own topics for discussion and discuss each topic at leisure
- _Productivity_: Gain an overall insight in to productivity via charts showing tickets raised over time

## Site Design

### Colour Scheme
A five colour palette was generated using [colormind.io](colormind.io) to ensure proper colour coordination. Full details in [palette.txt](palette.txt)

### Typography
Google Fonts: "Permanent Marker" (major headings), "Kalam" (sub headings and buttons), "Arsenal" (body text).
Cursive heading fonts used to reflect a comic book style.

### Wireframe Mockup
Mockup constructed using [WireframePro](https://mockflow.com/apps/wireframepro/) Version 3.0.9. see [wireframe.pdf](wireframe.pdf)

## Technology
- HTML, CSS, SCSS, JavaScript
- [Python](https://www.python.org) 3.7
- [jQuery](http://jquery.com) 3.3.1
- [Django](https://www.djangoproject.com) 2.0.7
- [Bootstrap](http://getbootstrap.com) 4.1.3
- [Chartist.js](https://gionkunz.github.io/chartist-js/)
- [moment.js](https://momentjs.com)
- [Stripe](https://js.stripe.com/v2/)
- [AWS S3](https://aws.amazon.com/s3/) for media hosting
- [Heroku](https://www.heroku.com) - deployed website

## Contribute
1. Ensure you have Python 3.7 installed
2. Set up a virtual environment using pip: `python3 -m venv .`
3. Clone github repository: `git clone https://github.com/julian-garcia/i-comic.git`
4. Run `python manage.py runserver` and the project will run on [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Testing
Forty tests have been implemented using the Django testing suite to test the various models, views and forms across all of the apps within this project. Test outcomes are available in [test_outcomes.txt](test_outcomes.txt). Travis CI is being used for continuous integration testing.

## Credits
### Media
Images retrieved from [Wikimedia Commons](https://commons.wikimedia.org/wiki/Main_Page) - these are freely reusable images
