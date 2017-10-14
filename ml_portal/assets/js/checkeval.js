
var refreshIntervalId;

$(function(){
  $('.evaluate-button').click(function(){
    startTraining();
    $('.evaluate-button').prop('disabled', true);
  });
});

function requestProgress() {
$.ajax({
    // la URL para la petición
    url : '/problems/evaluate/check/',
 
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

        if(json.progress >= 1.0){

          clearInterval(refreshIntervalId);
          $(".evaluate-prog").attr('style', "width:100%");
          $(".evaluate-prog").text( "100% Complete");
          $(".results").collapse('show');

          $(".step3").attr('class', 'col-xs-3 bs-wizard-step step3 complete');
          $(".step4").attr('class', 'col-xs-3 bs-wizard-step step4 active');
                    
        }else{
          var string = (json.progress * 100) + "";
          $(".evaluate-prog").attr('style', "width:" + string + "%");
          $(".evaluate-prog").text( string.substring(0,5) + "% Complete");
          $(".collapse container").collapse('hide');

        }
    },
 
    // código a ejecutar si la petición falla;
    // son pasados como argumentos a la función
    // el objeto de la petición en crudo y código de estatus de la petición
    error : function(xhr, status) {
        alert('Disculpe, existió un problema');
    },
 
    // código a ejecutar sin importar si la petición falló o no
    complete : function(xhr, status) {
        //alert('Petición realizada');
    }
});
};



function startTraining() {
$.ajax({
    // la URL para la petición
    url : '/problems/evaluate/start/',
 
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

        $(".progbar").collapse('toggle');
        refreshIntervalId=setInterval(function () {requestProgress()}, 3000);

    },
 
    // código a ejecutar si la petición falla;
    // son pasados como argumentos a la función
    // el objeto de la petición en crudo y código de estatus de la petición
    error : function(xhr, status) {
        alert('Disculpe, existió un problema');
    },
 
    // código a ejecutar sin importar si la petición falló o no
    complete : function(xhr, status) {
        //alert('Petición realizada');
    }
});
};


$(".prog-diag").collapse('show');