<?php
session_start(  );

require("model/Articulo.php");
require("model/Comentario.php");
require("../scripts/libs/conn.php");

##Building the connection handler.
$conn = Conn::Connect();

?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">    
<html>
<head>
   <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" >
	<link rel="icon" href="../favicon.ico" type="image/x-icon" >
	<link rel="shortcut icon" href="../favicon.ico" type="image/x-icon" >
	<meta id="description" content="el diletante digital (eldiletante.com) es el sitio Web del proyecto cubano homónimo dedicado al net.art, net-art, arte digital, hipertextos, literatura hipertextual, ciberliteratura, literatura digital, poesia electronica, literatura,  hacker, hacker art, hacker-art, arte de los nuevos medios y artes plasticas. Además proponemos un espacio para el diálogo teórico, subimos documentos sobre el movimiento de nuevos medios, concursos, becas, tenemos revistas digitales, en especial la revista Esfera." >
	<meta id="keywords" content="diletante digital, esquina13, hipertexto, literatura hipertextual, literatura digital, ciberliteratura, poesía electrónica, literatura colaborativa, net.art, net-art, hacker, hacker art, hacker-art, arte de los nuevos medios, new media, visual arts, plástica, cuba nuevos medios, teoria, estetica, filosofia, critica, ficcion, narrativa digital, revistas digitales cubanas, arte digital, artes plasticas, esfera, qubit, rockstalgias, disparo en red, minatura, arte cubano, cuentos eroticos, narraciones eroticas, historias eroticas, debate teórico, korad" >
	<title>Artículos - El Diletante Digital (eldiletante.com) es el sitio Web del proyecto cubano homónimo dedicado a la literatura hipertextual, la ciberliteratura, la literatura digital, la poesía electrónica, al net.art, net art, el hacker-art, hacker art, el arte de los nuevos medios, new media art y el arte digital en general. Además proponemos un espacio para el diálogo teórico, subimos documentos sobre el movimiento de nuevos medios en Cuba, artículos, críticas, concursos, becas, y tenemos una colección de revistas digitales. </title>
	<link rel="stylesheet" type="text/css" href="scripts/layout.css" media="screen, projection, tv " >
	<link rel="stylesheet" type="text/css" href="scripts/html.css" media="screen, projection, tv " >
	<script language="JavaScript1.2" src="../scripts/tools.js" type="text/javascript"></script>
	<link rel="stylesheet" type="text/css" href="../scripts/build/fonts/fonts-min.css" >
</head>

<body class=" yui-skin-sam">

<div id="content">
  <div id="header" class="width">  </div>
  <div id="headerImg" class="width"> </div>
  <div id="menu" class="width">

    <ul>
      <li>
        <a href="index.php" onfocus="blur()">
          <span class="title ">Lista </span>
          <span class="desc">Página de inicio, con lista de artículos.</span>        </a>      </li>
      <li>
        <a href="escribir_articulo.php" class="forum" onfocus="blur()">
          <span class="title ">Agregar Artículo</span>
          <span class="desc style3">Desde aquí puede subir sus textos.</span>        </a>      </li>
      <li>
        <a href="javascript:;"></a>      </li>

    </ul>
  </div>
  <div id="page">
    <div id="columns" class="widthPad">
    <div class="floatLeft width100">
    <h1>Página de Inicio.</h1>
    <p> Esta sección del sitio Web inaugura un espacio para que críticos, 
      teóricos y artistas publiquen  artículos, ensayos breves,
      o simplemente sus ideas. También se pueden dejar comentarios 
      al final de cada publicación. Este mecanismo sirve para debatir 
      opiniones, y para la necesaria retroalimentación con las ideas 
      de los demás. Para participar de este espacio (tanto para agregar artículos como comentarios) es necesario hacerse <a href="../gestion/login.php">usuario</a> del proyecto.</p>
    <p>Los artículos y comentarios publicados son de exclusiva responsabilidad 
      de sus autores. En este espacio se representa la opinión de los 
      usuarios y no de los creadores de El Diletante Digital.  No hay restricciones con respecto al tema, salvo en lo que toca a estos dos: están prohibidos 
      los debates políticos y religiosos, porque despiertan pasiones 
      poco edificantes. En los comentarios que se dejen no se aceptarán 
      insultos, ni agresiones personales de ningún tipo. Mantengamos 
      la compostura. <strong>Cualquier colaboración que rompa con alguna 
      de estas dos sencillas reglas, será inmediatamente borrada</strong>. 
      Y en este aspecto somos irreductibles. </p>
      <p> </p>
      <h1>Lista de Artículos.</h1>
      <?php
          $cuentosQuery = "SELECT ID, titulo, autor, cuerpo, fecha FROM articulos_colab";

          $rs = $conn->Execute($cuentosQuery) or die("<p class=\"mensaje\"><img src=\"../images/error.gif\" vspace=\"0\" hspace=\"10\" width=\"32\" heigth=\"32\" align=\"left\" > Error obtenidendo los artículos.<p>");

          echo "<ul>";
          while(!$rs->EOF){

           echo "<li>";
           echo "<b><a href=\"mostrar.php?ID=".$rs->Fields('ID')."\">".$rs->Fields('titulo')."</a></b>";
           echo " por ".$rs->Fields('autor');
           echo " (".$rs->Fields('fecha').")";
           echo "<br >";
           echo "</li>";

           $rs->MoveNext();
          }
          echo "</ul>";
          ?>
      <p> </p>
    </div>
    </div>
    
  </div>
  
</div>
<div id="footer">
  <div id="bg" class="width">
    <ul>
      <li><a href="../index.html">Inicio</a></li>
      <li><a href="../gestion/login.php">Usuarios</a></li>
	   <li><a href="../gestion/buscar.php">Buscar</a></li>
      <li><a href="../gestion/contactar.php" class="last">Contáctenos</a></li>
    </ul> 
  </div>

</div>
</body>
</html>
