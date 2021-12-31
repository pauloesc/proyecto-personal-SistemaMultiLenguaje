$(document).ready(function () {


    function ajax_login() {
        $.ajax({
        url: '/Administracion-CrearSeccion-Ajax',
        data: $('form').serialize(),
        type: 'POST',
        success: function (response) {
            console.log(response);

            if (response == []) {
                select = document.getElementById('pol');
                var opt = document.createElement('li');
                opt.className = "list-group-item";
                opt.innerHTML = 'No hay secciones o ocurrio un error';
                select.appendChild(opt);
            }
            else{
                $.each(response, function(i, item) {
                select = document.getElementById('pol');
                var opt = document.createElement('li');
                opt.className = "list-group-item";
                opt.innerHTML = item.dato;
                select.appendChild(opt);
            });
            }



        },
        error: function (error) {
            console.log(error);
        }
        });
    }


    $("#ajaxaccion").change(function() {
    ajax_login();
    });


});




function CrearIndice(pos) {

    var CrearFilaEnPosicion;



    if (pos != 'siguiente')
    {
        CrearFilaEnPosicion = pos;

        var totalFilas;
        totalFilas= 0;
        while ( document.getElementById( "fila["+(totalFilas+1)+"]" ))
        {
            totalFilas +=1;
        }

        while ( totalFilas >= pos )
        {
            //cambio cabecera
            cabecera = document.getElementById('fila['+(totalFilas)+']');
            cabecera.setAttribute('id','fila['+(totalFilas+1)+']');

            //cambio el numero de orden
            numero = document.getElementsByName('numero['+(totalFilas)+']')[0];
            numero.setAttribute('name', 'numero['+(totalFilas+1)+']' );
            numero.innerHTML = ''+(totalFilas+1)+'';

            //cambio los tipos
            tipo = document.getElementsByName('indice['+(totalFilas)+']')[0];
            tipo.setAttribute('name', 'indice['+(totalFilas+1)+']' );
            

            //cambio los estilos
            estilo = document.getElementsByName('nombre['+(totalFilas)+']')[0];
            estilo.setAttribute('name', 'nombre['+(totalFilas+1)+']' );



            //cambio boton
            boton = document.getElementsByName('eliminar['+(totalFilas)+']')[0];
            boton.setAttribute('onclick',"Eliminar("+(totalFilas+1)+")");
            boton.setAttribute('name','eliminar['+(totalFilas+1)+']');

            //cambio crear
            boton = document.getElementsByName('crear['+(totalFilas)+']')[0];
            boton.setAttribute('onclick',"CrearIndice("+(totalFilas+1)+")");
            boton.setAttribute('name','crear['+(totalFilas+1)+']');

            totalFilas-=1;
        }

    }
    else
    {
        CrearFilaEnPosicion = 1;

        while ( document.getElementById( "fila["+(CrearFilaEnPosicion)+"]" ))
        {
            CrearFilaEnPosicion +=1;
        }

    }


    // creo la fila
    var fila = document.createElement('tr');
    fila.setAttribute('id',"fila["+(CrearFilaEnPosicion)+"]");


    // primera columna
    var columna1 = document.createElement('td');

    //segunda columna
    var columna2 = document.createElement('td');

    // tercera columna
    var columna3 = document.createElement('td');

    // cuarta columna
    var columna4 = document.createElement('td');

    // cuarta quinta
    var columna5 = document.createElement('td');



    //contenido de la columna 1
    columna1.setAttribute('name','numero['+(CrearFilaEnPosicion)+']');
    columna1.innerHTML = CrearFilaEnPosicion;

    //contenido de la columna 2
    var indiceNumero = document.createElement('input');
    indiceNumero.setAttribute('class','form-control');
    indiceNumero.setAttribute('name','indice['+(CrearFilaEnPosicion)+']');

    //contenido de la columna 3
    var indiceNombre = document.createElement('input');
    indiceNombre.setAttribute('class','form-control');
    indiceNombre.setAttribute('name','nombre['+(CrearFilaEnPosicion)+']');

    //contenido de la columna 4
    var botonEliminar = document.createElement('input');
    botonEliminar.setAttribute('name','eliminar['+(CrearFilaEnPosicion)+']');
    botonEliminar.setAttribute('type','button');
    botonEliminar.setAttribute('value','Eliminar');
    botonEliminar.setAttribute('class','btn btn-primary');
    botonEliminar.setAttribute('onclick','Eliminar('+(CrearFilaEnPosicion)+')');

    var botonCrearDeterminadoIndice = document.createElement('input');
    botonCrearDeterminadoIndice.setAttribute('name','crear['+(CrearFilaEnPosicion)+']');
    botonCrearDeterminadoIndice.setAttribute('type','button');
    botonCrearDeterminadoIndice.setAttribute('value','Nueva fila');
    botonCrearDeterminadoIndice.setAttribute('onclick','CrearIndice('+(CrearFilaEnPosicion)+')');
    botonCrearDeterminadoIndice.setAttribute('class','btn btn-primary');



    //ensamblando
    columna2.appendChild(indiceNumero);
    columna3.appendChild(indiceNombre);
    columna4.appendChild(botonEliminar);
    columna5.appendChild(botonCrearDeterminadoIndice)

    fila.appendChild(columna1);
    fila.appendChild(columna2);
    fila.appendChild(columna3);
    fila.appendChild(columna4);
    fila.appendChild(columna5);


    tbody = document.getElementById('cuerpo');
    sssss = document.getElementById('cuerpo').childNodes[CrearFilaEnPosicion-1];
    console.log(sssss);
    console.log(CrearFilaEnPosicion);
    tbody.insertBefore(fila,sssss);

};




function Eliminar(vv) {

    var parrafo = document.getElementById("fila["+vv+"]");
    parrafo.parentNode.removeChild(parrafo);

    var totalContenido = 0;
    totalContenido = vv;

    while ( document.getElementById( 'fila['+(totalContenido+1)+']' ))
    {
        totalContenido += 1
    }


    while ( totalContenido > vv ) {

            //cambio cabecera
            cabecera = document.getElementById('fila['+(totalContenido)+']');
            cabecera.setAttribute('id','fila['+(totalContenido-1)+']');

            //cambio el numero de orden
            numero = document.getElementsByName('numero['+(totalContenido)+']')[0];
            numero.setAttribute('name', 'numero['+(totalContenido-1)+']' );
            numero.innerHTML = ''+(totalContenido-1)+'';

            //cambio los tipos
            tipo = document.getElementsByName('indice['+(totalContenido)+']')[0];
            tipo.setAttribute('name', 'indice['+(totalContenido-1)+']' );
            tipo.setAttribute('onclick', 'cambiarTipoContenido('+ (totalContenido-1) +') ');

            //cambio los estilos
            estilo = document.getElementsByName('nombre['+(totalContenido)+']')[0];
            estilo.setAttribute('name', 'nombre['+(totalContenido-1)+']' );

            //cambio boton
            boton = document.getElementsByName('eliminar['+(totalContenido)+']')[0];
            boton.setAttribute('onclick',"Eliminar("+(totalContenido-1)+")");
            boton.setAttribute('name','eliminar['+(totalContenido-1)+']');

            //cambio crear
            boton = document.getElementsByName('crear['+(totalContenido)+']')[0];
            boton.setAttribute('onclick',"CrearIndice("+(totalContenido-1)+")");
            boton.setAttribute('name','crear['+(totalContenido-1)+']');


        totalContenido -=1;
    }


};