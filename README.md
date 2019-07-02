# Site Survey Application

Application for doing site survey when planning electric vehicle charger installations.

## Design wireframes

[Design wireframes in Figma](https://www.figma.com/proto/cwyvzpbyNiWygBuhPAYOOvpF/SiteSurveyApp?node-id=0%3A1&scaling=scale-down)

## TODO:

### Survey
- [x] Add individual survey page
- [x] Link survey to location
- [ ] Add FileField to Survey form
- [ ] Add ability to save photos to harddrive
- [ ] Add work creation site
- [x] Add surveys to index page
- [ ] Add save to localStorage (JS) feature to survey
- [ ] Add Customer - Instalation switching animation to survey page
-> In main form create multiple (4?) contact persons but only toggle them as visible?
-> New form for each contact/location?
- [ ] Add filtering of locations
- [x] Sort out the many-to-many contact and location forms in survey. Possible?
- [ ] Embedding Google Maps / OpenStreetmap to enter coordinates?
- [x] Add status indication (created, waiting, ready) to survey table
### Account / Users
- [ ] Add email authentication to new users
- [ ] Highlight the nav user account so it's more noticeable (not clear it's clicable)
- [ ] Send sign up link on new user creation rather than entering password for user

### Chargers
- [ ] Tidy up the view chargers page formatting. Transposing the table for readability?

### Organizations
- [ ] Add listing of all organizations and link to individual organizations
- [ ] List users of organization

### General
- [ ] Update styling on all forms (submit button and fieldsets)
- [ ] User permissions
- [ ] Set up db check so you can initialize the app the first time. Currently it crashes on imports if no DB exists
