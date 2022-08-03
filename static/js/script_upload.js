// const form = document.querySelector("form");
// fileInput = document.querySelector(".file-input"),
const inputt = document.querySelector(".inputs")
const file_input = document.querySelector("#file_input");
let progressArea = document.querySelector(".progress-area");
let uploadedArea = document.querySelector(".uploaded-area");
const button = document.getElementById('btn')
const upload_file_name = document.getElementById('upload_fileName')

let uploaded_pdf
let body
let nam
let name_of_file

inputt.addEventListener("click", () =>{
  file_input.click();
});

button.addEventListener("click", upload)

file_input.addEventListener("change", ({target}) => {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
  uploaded_pdf = reader.result;
  console.log(typeof uploaded_pdf)
  console.log(uploaded_pdf)

  let file = target.files[0];
  if(file){
    let fileName = file.name;
    name_of_file = fileName
    upload_file_name.innerHTML = `${name_of_file} selected`
    if(fileName.length >= 12){
      let splitName = fileName.split('.');
      fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
    }
    nam = fileName
    console.log("File Name:"+ nam)
  // reader.fileName = file.name
  // reader.onload = function(file_name) {
  //   console.log(file_name.target.fileName)
  // }
  // document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})`;
  }
});
  reader.readAsDataURL(target.files[0]);
});

// fileInput.onchange = ({target})=>{
//   let file = target.files[0];
//   upload()
//   if(file){
//     let fileName = file.name;
//     if(fileName.length >= 12){
//       let splitName = fileName.split('.');
//       fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
//     }
//     uploadFile(fileName);
//   }
// }

function uploadFile(name){

  const datat = JSON.stringify(body)
  console.log(datat)

  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload_pdf', true)
  xhr.setRequestHeader('Content-Type', 'application/json')
  xhr.upload.addEventListener("progress", ({loaded, total}) =>{
    let fileLoaded = Math.floor((loaded / total) * 100);
    let fileTotal = Math.floor(total / 1000);
    let fileSize;
    (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024*1024)).toFixed(2) + " MB";
    let progressHTML = `<li class="row">
                          <i class="fas fa-file-alt"></i>
                          <div class="content">
                            <div class="details">
                              <span class="name">${name} • Uploading</span>
                              <span class="percent">${fileLoaded}%</span>
                            </div>
                            <div class="progress-bar">
                              <div class="progress" style="width: ${fileLoaded}%"></div>
                            </div>
                          </div>
                        </li>`;
    uploadedArea.classList.add("onprogress");
    progressArea.innerHTML = progressHTML;
    if(loaded == total){
      progressArea.innerHTML = "";
      let uploadedHTML = `<li class="row">
                            <div class="content upload">
                              <i class="fas fa-file-alt"></i>
                              <div class="details">
                                <span class="name">${name} • Uploaded</span>
                                <span class="size">${fileSize}</span>
                              </div>
                            </div>
                            <i class="fas fa-check"></i>
                          </li>`;
      uploadedArea.classList.remove("onprogress");
      uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
    }
  });
  // xhr.setRequestHeader("Content-Type", "application/")
  // let data = new FormData(form);
  xhr.send(datat);
}

function upload() {
  
  upload_file_name.innerHTML = `Browse File to Upload`
  base(name_of_file)

}

// async function api_call(){
//   const api_response = await fetch(`/upload`, { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json'}})
//   const response = await api_response.json()

//   console.log("api response"+ response)
//   // return response
// }

function toDataUrl(url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.onload = function() {
      var reader = new FileReader();
      reader.onloadend = function() {
          callback(reader.result);
      }
      reader.readAsDataURL(xhr.response);
  };
  xhr.open('GET', url);
  xhr.responseType = 'blob';
  xhr.send();
}

function base(nameFile) {
  var base64 = "base"
      toDataUrl(uploaded_pdf , function(myBase64) {
      console.log(myBase64); // myBase64 is the base64 string
      base64 = myBase64
  
      console.log('base64=' + base64);
      console.log(typeof base64)
  
      const base64_split = base64.split(",")[1]
      console.log(base64_split)
  
      body = {
          "pdf_name": nameFile,
          "pdf": base64_split
      }
  
      console.log(body)

      uploadFile(nam)
      // .then(resp => 
      //     update_refined_image(resp)
  
      // )
  
  })}