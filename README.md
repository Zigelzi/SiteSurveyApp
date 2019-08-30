# Site Survey Application

Application for doing site survey when planning electric vehicle charger installations.

## Design wireframes

[Design wireframes in Figma](https://www.figma.com/proto/cwyvzpbyNiWygBuhPAYOOvpF/SiteSurveyApp?node-id=0%3A1&scaling=scale-down)

## TODO:

### Survey
- [x] Add individual survey page
- [x] Link survey to location
- [x] Add FileField to Survey form
- [x] Add ability to save photos to harddrive
- [x] Add work creation site
- [x] Add surveys to index page
- [ ] Add save to localStorage (JS) feature to survey
- [ ] Add Customer - Installation switching animation to survey page
-> In main form create multiple (4?) contact persons but only toggle them as visible?
-> New form for each contact/location?
- [x] Add filtering of locations
- [x] Add dynamic field selection to charger
- [x] Sort out the many-to-many contact and location forms in survey. Possible?
- [ ] Embedding Google Maps / OpenStreetmap to enter coordinates?
- [x] Add status indication (created, waiting, ready) to survey table
- [ ] Add notice which fields are mandatory and which are not
- [ ] Need to emphasize that org and location are just search fields?
### Account / Users
- [x] Add email authentication to new users
- [ ] Highlight the nav user account so it's more noticeable (not clear it's clicable)
- [ ] Send sign up link on new user creation rather than entering password for user

### Products
- [ ] Tidy up the view chargers page formatting. Transposing the table for readability?
- [ ] Add the additional information of chargers to Product table

### Organizations
- [x] Add listing of all organizations and link to individual organizations
- [x] List users of organization

### General
- [x] Update styling on all forms (submit button and fieldsets)
- [ ] User permissions
- [x] Set up db check so you can initialize the app the first time. Currently it crashes on imports if no DB exists
- [ ] Make category creation more uniform (grey box vs fieldset)
- [ ] Rething the redirections of different pages
- [ ] Add back to menu button or cookiecrumbles
- [ ] Redo navigation in mobile and desktop
- [ ] Make secondary button for secondary actions like create organization type in create_organization route
- [ ] Add flashed messages to: 
- [ ] Add button to Organization for adding new contact persons
