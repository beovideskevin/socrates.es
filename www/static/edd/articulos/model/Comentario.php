<?php

class Comentario{

    private $origCuento;
    private $cuerpo;
    private $fecha;
    private $autor;



	function Comentario ( $a_orig, $a_autor, $a_cuerpo, $a_fecha)
	{
	   $this->origCuento = $a_orig;
	   $this->autor      = addslashes ($a_autor);
	   $this->cuerpo     = addslashes ($a_cuerpo);
	   $this->fecha      = $a_fecha;

	}


###Setters.
    public function setOrigArt($orig)
	{
	    $this->origCuento = $orig;
	}

	public function setCuerpo($cuerpo)
    {
	    $this->cuerpo = $cuerpo;
	}
	
	public function setFecha($fecha)
    {
	    $this->fecha = $fecha;
	}
	
	public function setAutor($autor)
    {
	    $this->autor = $autor;
	} 

### Getters.
    public function getOrigCuento()
	{
	    return $this->origCuento;
	}
	
	public function getCuerpo()
	{
		return $this->cuerpo;
	}
	
	public function getFecha()
	{
		return $this->fecha;
	}
	
	public function getAutor()
	{
		return $this->autor;
	}


###CRUDs.	
public function saveComentario($con)
{
    
	
      $saveQuery = "INSERT INTO articulos_comments ( idArticulo, autor, cuerpo, fecha)  VALUES ( '" . $this->getOrigCuento() . "','" . $this->getAutor() . "','" . $this->getCuerpo() . "','" . $this->getFecha() . "'    ) ";
								 							 
						
       $rs = $con->Execute($saveQuery) or die("<p class=\"error_msg\">Error accediendo a la base de datos!</p>");  						
	
	   return true;	 
	
  
}










}

?>
