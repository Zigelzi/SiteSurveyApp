import {getDataAddSuggestions} from './scripts.js';

document.addEventListener('DOMContentLoaded', () => {
    getDataAddSuggestions('/api/organizations', 'organizationList', 'org_name');
})