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
    let testJSON = {"products": [
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
    ]}

    // Function for requesting list of product data from backend and creating datalist based on them
    function addSuggestions() {
        const productList = document.getElementById('productList');

        // TODO: Request the product list from DB
        let response = testJSON;

        // Clear the previous suggestions from productList
        productList.innerHTML = "";

        response.products.forEach(item => {
            // Create new <option> element and append it to productList
            let option = document.createElement('option');
            option.value = item.productno;
            productList.appendChild(option);
        });
    }

    // Check that user has selected input that is in Datalist
    function onDatalistInput(event) {
        let tableRow = event.target.parentElement.parentElement;
        let productNo = event.target.value;
        const productList = document.getElementById('productList').childNodes;
        // Check if the productNo exists in the productList
        for (let i = 0; i < productList.length; i++) {
            if (productList[i].value === productNo) {
                // Take the full product data from JSON response
                fillTableData(tableRow, productNo);
                break;
            } else {
                // If the inputted productNo is not in the list zero the values
                tableRow.children[2].textContent = "--"; 
                tableRow.children[5].textContent = "--";  
            }
        }
    }

    // Take the full product data from JSON and add the information to table row.
    function fillTableData(tableRowElement, productNo) {
        for (let i = 0; i < testJSON.products.length; i++) {
            if (testJSON.products[i].productno === productNo) {
                let prodInfo = testJSON.products[i];
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
                    if (totalCellValue != "") {
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
            lastRowNo = 0;
        } else {
            columnCount = productBody.children[0].childElementCount;
            // Get the previous rows number (# column)
            lastRowNo = parseInt(productBody.lastElementChild.firstElementChild.textContent);
        }
              
        // Creating the td elements and their contents
        for (let i = 0; i < columnCount; i++) {
            let newCell = document.createElement('td');
            
            if (i === 0) {
                // Add current row number (previous row + 1)
                cellText = document.createTextNode(lastRowNo + 1);
                newCell.appendChild(cellText);
            }
            // Add additional elements and attributes to selected columns
            if (i === 1) {
                const textInput = document.createElement('input');
                const productList = document.getElementById('productList').id;
                textInput.type = "text";
                textInput.setAttribute('list', productList);
                textInput.className = 'productField';
                textInput.class
                newCell.appendChild(textInput);
                newCell.addEventListener('input', onDatalistInput);
                newCell.addEventListener('input', rowTotal);
            } 
            if (i === 3) {
                const numberInput = document.createElement('input')
                numberInput.type = "number";
                numberInput.className = 'amountField';
                newCell.appendChild(numberInput);
                newCell.addEventListener('input', rowTotal);
            }
            if (i === 4) {
                cellText = document.createTextNode('pcs');
                newCell.appendChild(cellText);
            }
            if (i === 6) {
                newCell.className = "totalColumn";
            }
            if (i === 7) {
                const trashIcon = document.createElement('img');
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

    addSuggestions()
    for (let i = 0; i < productField.length; i++) {
        productField[i].addEventListener('input', onDatalistInput);
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