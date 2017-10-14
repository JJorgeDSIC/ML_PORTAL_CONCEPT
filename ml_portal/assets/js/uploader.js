
function loadDropzone(json){

var previewNode = document.querySelector("#template");

previewNode.id = "";
var previewTemplate = previewNode.parentNode.innerHTML;
previewNode.parentNode.removeChild(previewNode);

var myDropzone = new Dropzone(document.body, { // Make the whole body a dropzone
    url: "/problems/upload_training/upload/", // Set the url
    thumbnailWidth: 80,
    thumbnailHeight: 80,
    parallelUploads: 1,
    previewTemplate: previewTemplate,
    autoQueue: false, // Make sure the files aren't queued until manually added
    previewsContainer: "#previews", // Define the container to display the previews
    clickable: ".fileinput-button", // Define the element that should be used as click trigger to select files.
    headers: {
      "X-CSRFToken" : csrftoken
    },
    success: function(file, response){

      if(response.success == true){
              //window.location="/validate_train/";
              file.previewElement.classList.add("dz-success");
              file.previewElement.querySelector("[data-dz-successmessage]").textContent = "Success !";

              $(".step1").attr('class', 'col-xs-3 bs-wizard-step step1 complete');
              $(".step2").attr('class', 'col-xs-3 bs-wizard-step step2 active');
              $(".step3").attr('class', 'col-xs-3 bs-wizard-step step3 disabled');
              $(".step4").attr('class', 'col-xs-3 bs-wizard-step step4 disabled');


          }else{

            var message = response.message;
            file.previewElement.classList.add("dz-error");
            file.previewElement.querySelector("[data-dz-errormessage]").textContent = message;

          }

          },

          error: function(file, response) {

            console.log(response)
           
            file.previewElement.classList.add("dz-error");
            file.previewElement.querySelector("[data-dz-errormessage]").textContent = "Unexpected Error";
        
      }
      
    });


 myDropzone.on("addedfile", function(file) {
    // Hookup the start button

    file.previewElement.querySelector(".start").onclick = function() { myDropzone.enqueueFile(file); };

    $('.fileinput-button').prop('disabled', true);
    $('.cancel').prop('disabled', false);

  });


 myDropzone.on("canceled", function(file) {
  console.log("cancelled");
  $('.fileinput-button').prop('disabled', false);
});

 myDropzone.on("removedfile", function(file) {
  console.log("removed");
  //Delete from server
  deleteFile();

  $(".step1").attr('class', 'col-xs-3 bs-wizard-step step1 active');
  $(".step2").attr('class', 'col-xs-3 bs-wizard-step step2 disabled');
  $(".step3").attr('class', 'col-xs-3 bs-wizard-step step3 disabled');
  $(".step4").attr('class', 'col-xs-3 bs-wizard-step step4 disabled');

  $('.traininginfo').collapse("hide");

  $('.fileinput-button').prop('disabled', false);
});

// Update the total progress bar
myDropzone.on("totaluploadprogress", function(progress) {
  //document.querySelector(".progress-bar").style.width = progress + "%";
  //$(".step3").attr('class', 'col-xs-3 bs-wizard-step step3 active');
  //$(".step4").attr('class', 'col-xs-3 bs-wizard-step step4 disabled');
});

myDropzone.on("sending", function(file) {
  // Show the total progress bar when upload starts

  // And disable the start button
  //file.previewElement.querySelector(".start").setAttribute("disabled", "disabled");
  $('.start').prop('disabled', true);
});



myDropzone.on("success", function(file) {
  console.log("success");
  $('.next').prop('disabled', false);
});


myDropzone.on("complete", function(file) {
    console.log("complete");
    $('.fileinput-button').prop('disabled', true);
  file.previewElement.classList.add("dz-success");
  //file.previewElement.querySelector("[data-dz-successmessage]").textContent = "Success !";
});

 
console.log(json);

if(json.filetitle != undefined){
  var mockFile = { name: json.filetitle, size: json.filesize };
  myDropzone.options.addedfile.call(myDropzone, mockFile);
  myDropzone.emit("complete", mockFile);
  //console.log(myDropzone);
  $('.traininginfo').collapse("show");
}

};


function requestUploadTrainingStatus() {

  $.ajax({
    // la URL para la petición
    url : '/problems/upload_training/check/',

    // la información a enviar
    // (también es posible utilizar una cadena de datos)
    data : { id : 123 },

    // especifica si será una petición POST o GET
    type : 'GET',

    // el tipo de información que se espera de respuesta
    dataType : 'json',

    // código a ejecutar si la petición es satisfactoria;
    // la respuesta es pasada como argumento a la función
    success : function(json) {


      console.log(json);



      loadDropzone(json);

    },

    // código a ejecutar si la petición falla;
    // son pasados como argumentos a la función
    // el objeto de la petición en crudo y código de estatus de la petición
    error : function(xhr, status) {
      console.log(xhr);
      console.log(status);
    },

    // código a ejecutar sin importar si la petición falló o no
    complete : function(xhr, status) {
        //alert('Petición realizada');
      }
    });


};

 
function deleteFile() {


  $.ajax({
    // la URL para la petición
    url : '/problems/upload_training/delete/',
    
    // la información a enviar
    // (también es posible utilizar una cadena de datos)
    data : { id : 123 },
    
    // especifica si será una petición POST o GET
    type : 'GET',
    
    // el tipo de información que se espera de respuesta
    dataType : 'json',
    
    // código a ejecutar si la petición es satisfactoria;
    // la respuesta es pasada como argumento a la función
    success : function(json) {

      console.log(json);
      $('.traininginfo').collapse("hide");
      
    },
    
    // código a ejecutar si la petición falla;
    // son pasados como argumentos a la función
    // el objeto de la petición en crudo y código de estatus de la petición
    error : function(xhr, status) {
      console.log(xhr);
      console.log(status);
    },
    
    // código a ejecutar sin importar si la petición falló o no
    complete : function(xhr, status) {
        //alert('Petición realizada');
      }
    });
};


requestUploadTrainingStatus();
$('.traininginfo').collapse("hide");