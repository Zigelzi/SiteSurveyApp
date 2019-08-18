/**
 * Get the data from backend with XHR and run the addSuggestion function to create <datalist> elements
 * @param {string} url target url where the data is fetched from
 * @param {string} elementId Target <datalist> element ID where <option> elements will be appended
 * @param {Object} jsonData JSON data which will be parsed to <option> elements
 * @param {string} dataKeyName Key name which will be used as the value attribute of <option> element
**/
function getDataAddSuggestions(url, elementId, dataKeyName) {
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const data = JSON.parse(xhr.responseText);
            addSuggestions(elementId, data, dataKeyName);
            console.log(`XHR ran for elementID ${elementId}`);
            }
        }
    xhr.open('GET', url);
    xhr.send();
}

function getData(url, callback) {
    const xhr = new XMLHttpRequest();

    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const data = JSON.parse(xhr.responseText);
            callback(data);
            }
        }
    xhr.open('GET', url);
    xhr.send();
}

function sendData(url, jsonObject, csrfToken=null) {
    const xhr = new XMLHttpRequest();
    const jsonData = JSON.stringify(jsonObject);

    xhr.open('POST', url);
    if (csrfToken !== null) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
    }
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.send(jsonData);
}

/** Validate that the users value entered to inputElementId is in the datalistId and then submit form
 * 
 * @param {string} inputElementId ElementID of the <input> element that user enters the value
 * @param {string} datalistId ElementID of the <datalist> element that the inputElementId is compared to
 */
function validateDatalistInput(inputElementId, datalistId) {
    const input = document.getElementById(inputElementId);
    const datalist = document.getElementById(datalistId);

    // If the input is in the datalist then submit the form
    for (let element of datalist.children) {
        if (element.value === input.value) {
            // console.log(element.value + 'in datalist')
            return true;
        }
    }
    // console.log(input.value + 'is not found from the list')
    return false;
}

/**  Function for parsing JSON object and creating <option> elements to the selected <datalist> element
 * @param {string} elementId Target <datalist> element ID where <option> elements will be appended
 * @param {Object} jsonData JSON data which will be parsed to <option> elements
 * @param {string} dataKeyName Key name which will be used as the value attribute of <option> element
 * 
**/
function addSuggestions(elementId, jsonData, dataKeyName) {
        const dataList = document.getElementById(elementId);
        let response = jsonData;

        // Clear the previous suggestions from dataList
        dataList.innerHTML = "";

        response.forEach(item => {
            // Create new <option> element and append it to dataList
            let option = document.createElement('option');
            option.value = item[dataKeyName];
            dataList.appendChild(option);
    });
}

export {getDataAddSuggestions, validateDatalistInput, getData, sendData};