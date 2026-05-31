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
	<title>Artículos - El Diletante Digital (eldiletante.com) es el sitio Web del proyecto cubano homónimo dedicado a la literatura hipertextual, la ciberliteratura, la literatura digital, la poesía electrónica, al net.art, net art, el hacker-art, hacker art, el arte de los nuevos medios, new media art y el arte digital en general. Además proponemos un espacio para el diálogo teórico, subimos documentos sobre el movimiento de nuevos medios en Cuba, artículos, críticas, concursos, becas, y tenemos una colecciónn de revistas digitales. </title>
	<link rel="stylesheet" type="text/css" href="scripts/layout.css" media="screen, projection, tv " >
	<link rel="stylesheet" type="text/css" href="scripts/html.css" media="screen, projection, tv " >
	<script language="JavaScript1.2" src="../scripts/tools.js" type="text/javascript"></script>
	<link rel="stylesheet" type="text/css" href="../scripts/build/fonts/fonts-min.css" >
	<link rel="stylesheet" type="text/css" href="../scripts/build/editor/assets/skins/sam/simpleeditor.css" >
	<link rel="stylesheet" type="text/css" href="../scripts/build/button/assets/skins/sam/button.css" >
	<script type="text/javascript" src="../scripts/build/yahoo-dom-event/yahoo-dom-event.js"></script>
	<script type="text/javascript" src="../scripts/build/element/element-beta-min.js"></script>
	<script type="text/javascript" src="../scripts/build/container/container_core-min.js"></script>
	<script type="text/javascript" src="../scripts/build/editor/simpleeditor-beta-min.js"></script>
	<script type="text/javascript" src="../scripts/build/button/button-min.js"></script>
	<script type="text/javascript" src="../scripts/build/yahoo/yahoo-min.js"></script>
	<script type="text/javascript" src="../scripts/build/event/event-min.js"></script>
	<script type="text/javascript" src="../scripts/build/dom/dom-min.js"></script>
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
      <li> <a id="nada" > </a> </li>
    </ul>
  </div>
  <div id="page">
    <div id="columns" class="widthPad">
    <div class="floatLeft width100">
        <h1 style="padding:20px 0 0 0;">Escribir Artículo.</h1>
        <?php
          if (isset ($_SESSION["login"])) {
        ?>
          <form name="demo" action="new_articulo.php" method="post" id="demo">
          <p>Título:<br >
          </p>
          <input type="text" id="tituloform" name="tituloform" size="40">
          <br >
          <br >
          <p>Autor (puede usar su nombre o un seudónimo):<br >
          </p>
          <input type="text" id="autor" name="autor"  size="40">
          <br >
          <br >
          <textarea id="cuerpo" name="cuerpo" rows="20" cols="75">
                   escriba el artículo aquí...
          </textarea>
          <p>Haga click aquí para guardar: 
            <input class="button" type="button" value="Guardar"
            onclick="save ();this.form.submit();" >
          </p>
        </form>
        <?php
            }else {
               echo "<p class=\"warning_msg\">Para dejar un artículo debe ser usuario del sitio, y haber entrado a su cuenta.</p>";
            }

           ?>
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
<script language="javascript1.2">

    var Dom = YAHOO.util.Dom,
        Event = YAHOO.util.Event;

    var myConfig = {
        height: '300px',
        width: '730px',
        dompath: true,
        focusAtStart: true
    };

    YAHOO.log('Create the Editor..', 'info', 'example');
    var myEditor = new YAHOO.widget.SimpleEditor('cuerpo', myConfig);
    myEditor.render();

    function save () {
      myEditor.saveHTML();
    }

</script>
</body>
</html>