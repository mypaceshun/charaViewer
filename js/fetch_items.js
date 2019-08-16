window.addEventListener("DOMContentLoaded", function() {
  for(let i = 0; i < 10; i++){
    const date_id = "date-" + i;
    const name_id = "name-" + i;
    const date_el = document.getElementById(date_id);
    const name_el = document.getElementById(name_id);

    date_el.addEventListener("change", function(){ fetch_items(i) });
    name_el.addEventListener("change", function(){ fetch_nums(i) });
    fetch_items(i);
    fetch_nums(i);
  }
});

async function fetch_items(num) {
  const date_el = document.getElementById("date-" + num);
  const name_el = document.getElementById("name-" + num);
  const num_el = document.getElementById("num-" + num);
  const empty_option = document.createElement("option");
  empty_option.selected = true;
  if(date_el.value == 0){
    name_el.innnerHTML = "";
    name_el.appendChild(empty_option);
    num_el.value = "";
  } else {
    endpoint = api_endpoint + "/" + date_el.value;
    console.log(endpoint);
    const res = await fetch(endpoint);
    const text = await res.json();
    const data = text["data"];
    name_el.innerHTML = "";
    name_el.appendChild(empty_option);
    for(let i = 0; i < data.length; i++){
      console.log(data[i]);
      const option = document.createElement("option");
      option.value = data[i]["name"];
      option.innerText = data[i]["text"];
      name_el.appendChild(option);
    }
  }
}

async function fetch_nums(num) {
  const date_el = document.getElementById("date-" + num);
  const name_el = document.getElementById("name-" + num);
  const num_el = document.getElementById("num-" + num);
  const empty_option = document.createElement("option");
  empty_option.selected = true;
  const max = 10;
  if(date_el.value == 0){
    num_el.value = "";
    num_el.max = max;
  } else {
    endpoint = api_endpoint + "/" + date_el.value;
    console.log(endpoint);
    const res = await fetch(endpoint);
    const text = await res.json();
    const data = text["data"];
    if(name_el.value == "null") {
        num_el.disabled = true;
        num_el.value = "";
    } else {
      let num = 0;
      for(let i = 0; i < data.length; i++){
        if(data[i]["num"] > 0){
          num = data[i]["num"];
          break;
        }
      }
      num_el.disabled = false;
      num_el.max = data[0]["num"];
    }
  }
}
