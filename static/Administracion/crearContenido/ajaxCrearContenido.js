function CrearCont(pos) {

    var CrearFilaEnPosicion;
    var totalFilas;

    if (pos != 'siguiente'){

        CrearFilaEnPosicion = pos;
        totalFilas = 0;

        while (document.getElementById("fila["+(totalFilas+1)+"]")) {
            totalFilas +=1;
        }

        while ( totalFilas >= pos ){

            //cambio cabecera
            cabecera = document.getElementById('fila['+(totalFilas)+']');
            cabecera.setAttribute('id','fila['+(totalFilas+1)+']');

            //cambio el numero de orden
            numero = document.getElementsByName('numero['+(totalFilas)+']')[0];
            numero.setAttribute('name', 'numero['+(totalFilas+1)+']' );
            numero.innerHTML = ''+(totalFilas+1)+'';

            //cambio los tipos
            tipo = document.getElementsByName('tipo['+(totalFilas)+']')[0];
            tipo.setAttribute('name', 'tipo['+(totalFilas+1)+']' );
            tipo.setAttribute('onclick', 'cambiarTipoContenido('+ (totalFilas+1) +') ');
            
            //cambio asignable
            asignable = document.getElementsByName('asignable['+(totalFilas)+']')[0];
            asignable.setAttribute('name', 'asignable['+(totalFilas+1)+']' );

            //cambio html apertura
            asignable = document.getElementsByName('htmlAp['+(totalFilas)+']')[0];
            asignable.setAttribute('name', 'htmlAp['+(totalFilas+1)+']' );

            //cambio contenido
            contenido = document.getElementsByName('contenido['+(totalFilas)+']')[0];
            contenido.setAttribute('name', 'contenido['+(totalFilas+1)+']' );

            //cambio html cierre
            asignable = document.getElementsByName('htmlCi['+(totalFilas)+']')[0];
            asignable.setAttribute('name', 'htmlCi['+(totalFilas+1)+']' );

            //cambio boton
            boton = document.getElementsByName('eliminar['+(totalFilas)+']')[0];
            boton.setAttribute('onclick',"Eliminar("+(totalFilas+1)+")");
            boton.setAttribute('name','eliminar['+(totalFilas+1)+']');

            //cambio crear
            boton = document.getElementsByName('crear['+(totalFilas)+']')[0];
            boton.setAttribute('onclick',"CrearCont("+(totalFilas+1)+")");
            boton.setAttribute('name','crear['+(totalFilas+1)+']');

            totalFilas-=1;
        }
    }

    else{

        CrearFilaEnPosicion = 1;
        while ( document.getElementById( "fila["+(CrearFilaEnPosicion)+"]" )) {
            CrearFilaEnPosicion +=1;
        }

    }


    // creo la fila ------------------------------------------------------------------
    var fila = document.createElement('tr');
    fila.setAttribute('id',"fila["+(CrearFilaEnPosicion)+"]");


    // primera columna ------------------------------------------------------------------
    var columna1 = document.createElement('td');
    columna1.setAttribute('name','numero['+(CrearFilaEnPosicion)+']');
    columna1.innerHTML = (CrearFilaEnPosicion);


    //segunda columna ------------------------------------------------------------------
    var columna2 = document.createElement('td');

    opcionesTipoContenido = document.createElement('select');
    opcionesTipoContenido.setAttribute('class','form-control');
    opcionesTipoContenido.setAttribute('multiple','');
    opcionesTipoContenido.setAttribute('name','tipo['+(CrearFilaEnPosicion)+']');
    opcionesTipoContenido.setAttribute('onclick','cambiarTipoContenido('+ CrearFilaEnPosicion +')');

    datos_para_columna = document.createElement('option');
    datos_para_columna.value = 'Texto';
    datos_para_columna.innerHTML = 'Texto';
    opcionesTipoContenido.appendChild(datos_para_columna);

    datos_para_columna = document.createElement('option');
    datos_para_columna.value = 'Imagen';
    datos_para_columna.innerHTML = 'Imagen';
    opcionesTipoContenido.appendChild(datos_para_columna);

    datos_para_columna = document.createElement('option');
    datos_para_columna.value = 'Audio';
    datos_para_columna.innerHTML = 'Audio';
    opcionesTipoContenido.appendChild(datos_para_columna);

    datos_para_columna = document.createElement('option');
    datos_para_columna.value = 'Video';
    datos_para_columna.innerHTML = 'Video';
    opcionesTipoContenido.appendChild(datos_para_columna);

    columna2.appendChild(opcionesTipoContenido);

    // tercera columna ------------------------------------------------------------------
    var columna3 = document.createElement('td');
    
    opcionesAsignable = document.createElement('select');
    opcionesAsignable.setAttribute('class','form-control');
    opcionesAsignable.setAttribute('name','asignable['+(CrearFilaEnPosicion)+']');

    datos_para_columna = document.createElement('option');
    datos_para_columna.value = 'si';
    datos_para_columna.innerHTML = 'si';
    opcionesAsignable.appendChild(datos_para_columna);

    datos_para_columna = document.createElement('option');
    datos_para_columna.value = 'no';
    datos_para_columna.innerHTML = 'no';
    opcionesAsignable.appendChild(datos_para_columna);

    columna3.appendChild(opcionesAsignable);

//--------------------------------------------
    var columna4 = document.createElement('td');
    contenido = document.createElement('input');
    contenido.setAttribute('class','form-control');
    contenido.setAttribute('name','htmlAp['+(CrearFilaEnPosicion)+']');
    contenido.setAttribute('type','text');
    columna4.appendChild(contenido);




    // cuarta columna ------------------------------------------------------------------
    var columna5 = document.createElement('td');
    
    contenido = document.createElement('input');
    contenido.setAttribute('class','form-control');
    contenido.setAttribute('name','contenido['+(CrearFilaEnPosicion)+']');
    contenido.setAttribute('type','text');
    columna5.appendChild(contenido);


    var columna6 = document.createElement('td');
    contenido = document.createElement('input');
    contenido.setAttribute('class','form-control');
    contenido.setAttribute('name','htmlCi['+(CrearFilaEnPosicion)+']');
    contenido.setAttribute('type','text');
    columna6.appendChild(contenido);


    // quinta columna ------------------------------------------------------------------
    var columna7 = document.createElement('td');
    
    botonEliminar = document.createElement('input');
    botonEliminar.setAttribute('name','eliminar['+(CrearFilaEnPosicion)+']');
    botonEliminar.setAttribute('type','button');
    botonEliminar.setAttribute('value','Eliminar');
    botonEliminar.setAttribute('onclick','Eliminar('+(CrearFilaEnPosicion)+')');
    botonEliminar.setAttribute('class','btn btn-primary');
    columna7.appendChild(botonEliminar);

    botonCrearDeterminadaPos = document.createElement('input');
    botonCrearDeterminadaPos.setAttribute('name','crear['+(CrearFilaEnPosicion)+']');
    botonCrearDeterminadaPos.setAttribute('type','button');
    botonCrearDeterminadaPos.setAttribute('value','Nueva fila');
    botonCrearDeterminadaPos.setAttribute('onclick','CrearCont('+(CrearFilaEnPosicion)+')');
    botonCrearDeterminadaPos.setAttribute('class','btn btn-primary');
    columna7.appendChild(botonCrearDeterminadaPos);


    // Anado las columnas a la fila------------------------------------------------------------------
    fila.appendChild(columna1);
    fila.appendChild(columna2);
    fila.appendChild(columna3);
    fila.appendChild(columna4);
    fila.appendChild(columna5);
    fila.appendChild(columna6);
    fila.appendChild(columna7);


    tbody = document.getElementById('cuerpo');
    sssss = document.getElementById('cuerpo').childNodes[CrearFilaEnPosicion-1];
    tbody.insertBefore(fila,sssss);

};

// ------------------------------------------------------------------
// ------------------------------------------------------------------
// ------------------------------------------------------------------

function Eliminar(vv) {

    var FilaAEliminar = document.getElementById("fila["+vv+"]");
    FilaAEliminar.parentNode.removeChild(FilaAEliminar);

    var totalContenido = 0;
    totalContenido = vv;

    while ( document.getElementById( 'fila['+(totalContenido+1)+']' )){
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
            tipo = document.getElementsByName('tipo['+(totalContenido)+']')[0];
            tipo.setAttribute('name', 'tipo['+(totalContenido-1)+']' );
            tipo.setAttribute('onclick', 'cambiarTipoContenido('+ (totalContenido-1) +') ');

            //cambio asignable
            asignable = document.getElementsByName('asignable['+(totalContenido)+']')[0];
            asignable.setAttribute('name', 'asignable['+(totalContenido-1)+']' );

                //cambio asignable
                asignable = document.getElementsByName('htmlAp['+(totalContenido)+']')[0];
                asignable.setAttribute('name', 'htmlAp['+(totalContenido-1)+']' );

            //cambio contenido
            contenido = document.getElementsByName('contenido['+(totalContenido)+']')[0];
            contenido.setAttribute('name', 'contenido['+(totalContenido-1)+']' );

                //cambio asignable
                asignable = document.getElementsByName('htmlCi['+(totalContenido)+']')[0];
                asignable.setAttribute('name', 'htmlCi['+(totalContenido-1)+']' );

            //cambio boton
            boton = document.getElementsByName('eliminar['+(totalContenido)+']')[0];
            boton.setAttribute('onclick',"Eliminar("+(totalContenido-1)+")");
            boton.setAttribute('name','eliminar['+(totalContenido-1)+']');

            //cambio crear
            boton = document.getElementsByName('crear['+(totalContenido)+']')[0];
            boton.setAttribute('onclick',"CrearCont("+(totalContenido-1)+")");
            boton.setAttribute('name','crear['+(totalContenido-1)+']');


        totalContenido -=1;
    }


};





















function cambiarTipoContenido(pos) {

    var cambiarAsignable = document.getElementsByName('asignable['+pos+']')[0];
    var cambiarTipo = document.getElementsByName('contenido['+pos+']')[0];
    var tipoContenido = document.getElementsByName('tipo['+pos+']')[0].value;
    
    if (tipoContenido == 'Texto'){
        cambiarAsignable.value='si';
        cambiarTipo.setAttribute('type','text');
    }
    else{
        cambiarAsignable.value='no';
        cambiarTipo.setAttribute('type','file');
    }

 };
















