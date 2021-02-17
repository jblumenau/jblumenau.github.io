let jsondata;
fetch("https://www.jackblumenau.com/data/conjoint_test.json")
  .then(res => res.json())
  .then(output => {
  	var items = output;
  	var item = random_item(items);
  	console.log(item);
	document.getElementById("json").textContent = JSON.stringify(item, null, 4);
  }
  )
  