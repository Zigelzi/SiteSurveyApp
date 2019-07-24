document.addEventListener('DOMContentLoaded', () => {

    const productField = document.getElementById('productField')
    const amountField = document.getElementById('amountField');
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
                tableRow.children[2].textContent = "-"; 
                tableRow.children[5].textContent = "-";  
            }
        }
    }

    // Take the full product data from JSON and add the information to table row.
    function fillTableData(tableRowElement, productNo) {
        for (let i = 0; i < testJSON.products.length; i++) {
            if (testJSON.products[i].productno === productNo) {
                let prodInfo = testJSON.products[i];
                tableRowElement.children[2].textContent = prodInfo.manufacturer + " " + prodInfo.model;
                tableRowElement.children[5].textContent = prodInfo.price;
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
            rowTotalTd.textContent = 0;
        }
    }

    // Calculate the complete order total to tfoot
    function tableTotal(mutations) {
        const tableTotalTd = document.getElementById('tableTotalTd')
        let totalSum = 0;
        mutations.forEach(function(mutation) {
            if (mutation.target.className === 'totalColumn') {
                const productBody = mutation.target.parentElement.parentElement;
                for (let i = 0; i < productBody.children.length; i++) {
                    totalSum += parseFloat(productBody.children[i].children[6].textContent.replace(",",".").replace(' ',''));
                }
            }       
        });
        tableTotalTd.textContent = totalSum + " €";
    }

    function addRow(event) {
        const tableRow = event.target;
        let newRow = document.createElement('tr')
        let newColumn = document.createElement('td')
        newRow.appendChild(newColumn);
        productBody.appendChild(newRow);
        console.log(tableRow);
    }

    addSuggestions()
    productField.addEventListener('input', onDatalistInput);
    productField.addEventListener('input', rowTotal);
    amountField.addEventListener('input', rowTotal);
    addTableRow.addEventListener('click', addRow)
})