document.addEventListener('DOMContentLoaded', () => {

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

    // Test JSON. Replace this with AJAX-call from DB.
    const testJSON = [
        {
            "productno":"cnd-1000",
            "manufacturer":"ensto",
            "model":"evf200",
            "price":2200
        },
        {
            "productno":"cnd-2000",
            "manufacturer":"tritium",
            "model":"veefil",
            "price":30000
        }
    ]

    const customerJSON = [
        {
            "org_name":"Example Ltd",
            "org_number": "124567-8",
            "address": "Example Str 1",
            "postal_code": "00000",
            "city": "Example",
            "country": "Finland"
        },
        {
            "org_name":"Markun Rengas Oy",
            "org_number": "124567-1",
            "address": "Markuntie 1",
            "postal_code": "08500",
            "city": "Lohja",
            "country": "Finland"
        }
    ]

    function innerFunc (arg1, arg2, arg3) {
        console.log(`Got following arguments: ${arg1}, ${arg2}, ${arg3}`)
    }
    function testFunc(url, arg1, arg2, arg3) {
        console.log(`Beep beep, sending data to ${url}`);
        innerFunc(arg1, arg2, arg3);
    }

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
                console.log(element.value + 'in datalist')
                return true;
            }
        }
        console.log(input.value + 'is not found from the list')
        return false;
    }

    // Check that user has selected input that is in Datalist
    function validateTableDataInput(event) {
        let tableRow = event.target.parentElement.parentElement;
        let productNo = event.target.value;
        const productList = document.getElementById('productList').childNodes;
        // Check if the productNo exists in the productList
        for (let i = 0; i < productList.length; i++) {
            if (productList[i].value === productNo) {
                // Take the full product data from JSON response
                fillTableData(tableRow, productNo, testJSON);
                break;
            } else {
                // If the inputted productNo is not in the list zero the values
                tableRow.children[2].textContent = "--"; 
                tableRow.children[5].textContent = "--";  
            }
        }
    }

    function fillTableData(tableRowElement, productNo, productJson) {
        // Take the full product data from JSON and add the information to table row.
        for (let i = 0; i < productJson.length; i++) {
            if (productJson[i].productno === productNo) {
                let prodInfo = productJson[i];
                tableRowElement.children[2].textContent = prodInfo.manufacturer + " " + prodInfo.model;
                tableRowElement.children[5].textContent = prodInfo.price + " €";
            }
        }
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
        const tableTotalTd = document.getElementById('tableTotalTd')
        let totalSum = 0;

        // Looping through all the happened mutations and performing task based on mutation target
        mutations.forEach(function(mutation) {
            // If total column sum changes (changed product or amount), recalculate the total order sum in tfoot.
            if (mutation.target.className === 'totalColumn') {
                const productBody = mutation.target.parentElement.parentElement;
                let totalCellValue
                for (let i = 0; i < productBody.children.length; i++) {
                    totalCellValue = productBody.children[i].children[6].textContent
                    if (totalCellValue != "--" && totalCellValue != "NaN €") {
                        totalSum += parseFloat(productBody.children[i].children[6].textContent.replace(",",".").replace(' ',''));
                    }
                }
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
        tableTotalTd.textContent = totalSum + " €";
    }

    function addRow() {
        const newRow = document.createElement('tr');
        let columnCount;
        let lastRowNo;
        let cellText;  

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
                //cellText = document.createTextNode(lastRowNo + 1);
                //newCell.appendChild(cellText);
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
                newCell.addEventListener('input', validateTableDataInput);
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

    addSuggestions('productList', testJSON, 'productno')
    addSuggestions('customerList', customerJSON, 'org_name')
    getDataAddSuggestions('/api/locations', 'locationList', 'address');

    for (let i = 0; i < productField.length; i++) {
        productField[i].addEventListener('input', validateTableDataInput);
        productField[i].addEventListener('input', rowTotal);
    }
    for (let i = 0; i < amountField.length; i++) {
        amountField[i].addEventListener('input', rowTotal);
    }
    for (let i = 0; i < deleteRow.length; i++) {
        deleteRow[i].addEventListener('click', removeRow);
    }
    addTableRow.addEventListener('click', addRow)
})