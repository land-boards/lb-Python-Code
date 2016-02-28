	(function (document) {
	  
	  var run = function (rawOrderObject) {
	  
	  var orderObject;
	  
	  try {
		orderObject = JSON.parse(rawOrderObject);
	  } catch (e) {
		alert("Could not read order object!\n" + e);
		return;
	  }
	  
	  var menu = document.getElementById('deliveryAddressCountryId-menu');
	  
	  for (var i = 0; i < menu.children.length; i += 1) {
	    var listItem = menu.children[i];
		
		if (listItem.innerHTML.toUpperCase().indexOf(orderObject["Country"].toUpperCase()) !== -1) {
			/* For some reason the element needs to be re-gotten */
			document.getElementById(listItem.id).click();
			break;
		}
	  }
	  
	  setTimeout(function () {

	  [
		{
		  elementId: 'deliveryAddressFirstName',
		  key: 'First Name'
		},
		{
		  elementId: 'deliveryAddressLastName',
		  key: 'Last Name'
		},
		{
		  elementId: 'deliveryAddressMiddleInit',
		  key: 'MI'
		},
		{
		  elementId: 'deliveryAddressCompany',
		  key: 'Company'
		},
		{
		  elementId: 'deliveryAddressLine1Addr',
		  key: 'Address 1'
		},
		{
		  elementId: 'deliveryAddressLine2Addr',
		  key: 'Address 2'
		},
		{
		  elementId: 'deliveryAddressLine3Addr',
		  key: 'Address 3'
		},
		{
		  elementId: 'deliveryAddressCityName',
		  key: 'City'
		},
		{
		  elementId: 'deliveryAddressPostalCode',
		  key: 'ZIP/Postal Code'
		},
		{
		  elementId: 'deliveryAddressProvince',
		  key: 'State/Province'
		}
	  ].forEach(function (args) {
		document.getElementById(args.elementId).value = orderObject[args.key];
	  });
	  
	  [
	    {
		  elementId: 'ounces',
		  staticValue: '2'
		},
		{
		  elementId: 'pkgValueAmt',
		  staticValue: '12.00'
		}
	  ].forEach(function (args) {
		document.getElementById(args.elementId).value = args.staticValue;
	  });
	  
	  menu = document.getElementById('serviceType-menu');
	  
	  for (var i = 0; i < menu.children.length; i += 1) {
	    var listItem = menu.children[i];
		
		if (listItem.innerHTML.indexOf("First") === 0) {
			listItem.click();
			break;
		}
	  }

	  }, 500);
	  };
	  
	  if (document.URL.indexOf('labelInformation') !== -1) {
	    var rawOrderObject = prompt("Please paste an order object");
	  
	    run(rawOrderObject);
	    setTimeout(function () {
		  run(rawOrderObject);
	    }, 500);
	  
	    setTimeout(function () {
		  run(rawOrderObject);
	    }, 1000);
	  
	    setTimeout(function () {
	      document.getElementById('getPricesButtonWrapper').children[0].children[0].children[0].click();
	    }, 1500);
	  }
	  
	  if (document.URL.indexOf('customsInformation') !== -1) {
	    document.getElementById('contents').value = 'MERCHANDISE';
		document.getElementById('itemDesc').value = 'Electronic card';
		document.getElementById('unitValue').value = '12.00';
		document.getElementById('itemQty').value = '1';
		document.getElementById('ounces').value = '2';
		document.getElementById('eelCode').value = 'NOEEI 30.37(a)';
	  }
	  
	})(document);