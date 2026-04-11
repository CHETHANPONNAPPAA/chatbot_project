function predict(){
fetch("http://127.0.0.1:5001/predict",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
Age:parseInt(age.value),
Gender:gender.value==="Male"?1:0
})
})
.then(r=>r.json())
.then(d=>result.innerText=d.result);
}