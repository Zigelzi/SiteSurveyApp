import {getDataAddSuggestions, getData, validateDatalistInput} from './scripts.js';

document.addEventListener('DOMContentLoaded', () => {

    // Input and information elements
    const orgInput = document.getElementById('orgInput');
    const contactPersonInfo = document.getElementById('contactPerson');
    const contactPersonArray = Array.from(contactPersonInfo.children);
    const locationInput = document.getElementById('locationInput');
    const locationInfo = document.getElementById('locationInformation');
    const locationInfoArray = Array.from(locationInfo.children);

    // Table elements
    const productField = document.getElementsByClassName('productField');
    const amountField = document.getElementsByClassName('amountField');
    const deleteRow = document.getElementsByClassName('deleteRow');
    const productBody = document.getElementById('productBody');
    const addTableRow = document.getElementById('addTableRow');

    /* Create MutationObserver to observe changes in productBody for calculating
     the order total*/ 
    let observer = new MutationObserver(tableTotal)
    let mutationConfig = {attributes: true, childList:true, characterData: true, subtree:true}
    observer.observe(productBody, mutationConfig);

    // Check that user has selected input that is in Datalist
    function validateTableDataInput(event) {
        let productNo = event.target.value;
        const productList = document.getElementById('productList').childNodes;
        // Check if the productNo exists in the productList
        for (let i = 0; i < productList.length; i++) {
            if (productList[i].value === productNo) {
                return true;
            } 
        }
        return false;
    }

    // Calculate the row total
    function rowTotal(event) {
        let tableRow = event.target.parentElement.parentElement;
        let amount = parseInt(event.target.value);
        let price = parseFloat(tableRow.children[5].textContent.replace(",",".").replace(' ',''));
        let rowTotalTd = tableRow.children[6];
        if (amount >= 0) {
            rowTotalTd.textContent = amount * price + " €";
        } else {
            rowTotalTd.textContent = 0 + " €";
        }
    }

    // Calculate the complete order total to tfoot
    function tableTotal(mutations) {

        // Looping through all the happened mutations and performing task based on mutation target
        mutations.forEach(function(mutation) {
            // If total column sum changes (changed product or amount), recalculate the total order sum in tfoot.
            if (mutation.target.className === 'totalColumn') {
                const productBody = mutation.target.parentElement.parentElement;
                let totalCellValue
                const tableTotalTd = document.getElementById('tableTotalTd')
                let totalSum = 0;
                for (let i = 0; i < productBody.children.length; i++) {
                    totalCellValue = productBody.children[i].children[6].textContent
                    // console.log(`Mutation: ${mutation.target.className}`);
                    if (totalCellValue != "--" && totalCellValue != "NaN €") {
                        totalSum += parseFloat(productBody.children[i].children[6].textContent.replace(",",".").replace(' ',''));
                    }
                }
                tableTotalTd.textContent = totalSum + " €";
            }
            // If table rows get removed redo the running numbering of rows
            if (mutation.removedNodes.length !== 0) {
                if (mutation.removedNodes[0].nodeName === 'TR') {
                    const tableRows = productBody.children;
                    // Loop though all the rows
                    for (let i = 0; i < productBody.childElementCount; i++) {
                        // Replace the first td (index = 0) value with running numbering
                        tableRows[i].children[0].textContent = i + 1;
                    }
                }  
            }   
        });
    }

    function addRow() {
        const newRow = document.createElement('tr');
        let columnCount;
        let lastRowNo;
        // Check if there's existing rows in the table. If not, then create first row
        if (productBody.children.length === 0) {
            columnCount = 8;
            lastRowNo = 1;
        } else {
            columnCount = productBody.children[0].childElementCount;
            // Get the previous rows number (# column)
            lastRowNo = parseInt(productBody.lastElementChild.firstElementChild.textContent);
            lastRowNo += 1;
        }
              
        // Creating the td elements and their contents
        for (let i = 0; i < columnCount; i++) {
            let newCell = document.createElement('td');
            newCell.textContent = '--'
            
            if (i === 0) {
                // Add current row number (previous row + 1)
                newCell.textContent = lastRowNo
            }
            // Add additional elements and attributes to selected columns
            if (i === 1) {
                const textInput = document.createElement('input');
                const productList = document.getElementById('productList').id;
                newCell.textContent = ''
                textInput.type = "text";
                textInput.setAttribute('list', productList);
                textInput.className = 'productField';
                newCell.appendChild(textInput);
                newCell.addEventListener('input', event => {
                    let tableRow = event.target.parentElement.parentElement;
                    if (validateTableDataInput(event)) {
                        getData(`/api/product/${event.target.value}`, data => {
                            tableRow.children[2].textContent = data.product_name; // Product column
                            tableRow.children[4].textContent = data.unit_of_material; // UOM column
                            tableRow.children[5].textContent = data.price + " €"; // Price column
                        })
                    } else {
                        // If the inputted product number is not in the list zero the values
                        tableRow.children[2].textContent = "--"; // Product column
                        tableRow.children[4].textContent = "--"; // UOM column
                        tableRow.children[5].textContent = "--"; // Price column
                    }
                });
                newCell.addEventListener('input', rowTotal);
            } 
            if (i === 3) {
                const numberInput = document.createElement('input')
                newCell.textContent = ''
                numberInput.type = "number";
                numberInput.className = 'amountField';
                newCell.appendChild(numberInput);
                newCell.addEventListener('input', rowTotal);
            }
            if (i === 6) {
                newCell.textContent = '--'
                newCell.className = "totalColumn";
            }
            if (i === 7) {
                const trashIcon = document.createElement('img');
                newCell.textContent = ''
                trashIcon.src = '/static/img/icon_trash.svg';
                trashIcon.alt = 'Trash bin icon';
                trashIcon.className = 'icon-small';
                newCell.appendChild(trashIcon);
                newCell.addEventListener('click', removeRow);
                
            }
            newRow.appendChild(newCell);                 
        }
        productBody.appendChild(newRow);
    }

    // Callback to remove the clicked row
    function removeRow(event) {
        if (event.target.nodeName === 'IMG') {
            const table = document.getElementById('productTable');
            const row = event.target.parentElement.parentElement;
            table.deleteRow(row.rowIndex);
        } 
    }

    getDataAddSuggestions('/api/locations', 'locationList', 'name');
    getDataAddSuggestions('/api/customers', 'customerList', 'org_name');
    getDataAddSuggestions('/api/products', 'productList', 'product_number');

    for (let i = 0; i < productField.length; i++) {
        productField[i].addEventListener('input', event => {
            let tableRow = event.target.parentElement.parentElement;
            if (validateTableDataInput(event)) {
                getData(`/api/product/${event.target.value}`, data => {
                    tableRow.children[2].textContent = data.product_name; // Product column
                    tableRow.children[4].textContent = data.unit_of_material; // UOM column
                    tableRow.children[5].textContent = data.price + " €"; // Price column
                })
            } else {
                // If the inputted product number is not in the list zero the values
                tableRow.children[2].textContent = "--"; // Product column
                tableRow.children[4].textContent = "--"; // UOM column
                tableRow.children[5].textContent = "--"; // Price column
            }
        });
        productField[i].addEventListener('input', rowTotal);
    }
    for (let i = 0; i < amountField.length; i++) {
        amountField[i].addEventListener('input', rowTotal);
    }
    for (let i = 0; i < deleteRow.length; i++) {
        deleteRow[i].addEventListener('click', removeRow);
    }
    addTableRow.addEventListener('click', addRow)
    locationInput.addEventListener('input', (event) => {
        const inputElementId = event.target.id;
        // If value from customer <input> field is in the datalist query the full information from backend via API
        if (validateDatalistInput(inputElementId, 'locationList')) {
            getData(`/api/location/${event.target.value}`, data => {
                locationInfoArray[1].textContent = `${data.address}`; // Address field
                locationInfoArray[2].textContent = `${data.postal_code} ${data.city}`; // Postal field
                locationInfoArray[3].textContent = `${data.country}`; // Country field
                locationInfoArray[4].textContent = `Lat: ${data.coordinate_lat} Long: ${data.coordinate_long}`; // Coordinates field
            });
        } else {
            locationInfoArray[1].textContent = 'Address'
            locationInfoArray[2].textContent = 'Postal'
            locationInfoArray[3].textContent = 'Country'
            locationInfoArray[4].textContent = 'Coordinates'
        }
    });

    orgInput.addEventListener('input', event => {
        const inputElementId = event.target.id;
        // If value from customer <input> field is in the datalist query the full information from backend via API
        if (validateDatalistInput(inputElementId, 'customerList')) {
            getData(`/api/organization/${event.target.value}`, data => {
                if (typeof data.contact_persons[0] != 'undefined') {
                    contactPersonArray[1].textContent = `${data.contact_persons[0].first_name} ${data.contact_persons[0].last_name}`;
                    contactPersonArray[2].textContent = `${data.contact_persons[0].phone_number}`;
                    contactPersonArray[3].textContent = `${data.contact_persons[0].email}`;
                }
            });
        } else {
            contactPersonArray[1].textContent = 'Firstname Lastname';
            contactPersonArray[2].textContent = 'Phone number';
            contactPersonArray[3].textContent = 'Email';
        }
    })
})