<?php
	
	
class Articulo {
	
	private $titulo;
	private $autor;
	private $cuerpo;
	private $fecha;
	

	
	function Articulo($a_titulo, $a_autor, $a_cuerpo, $a_fecha)
	{
	   
	   //if(empty($a_fecha)) { $fecha = date("m/d/y"); }
	   //else{ $fecha = $a_fecha; }
	    
	   $this->titulo = addslashes ($a_titulo);
	   $this->autor   = addslashes ($a_autor);
	   $this->cuerpo  = addslashes ($a_cuerpo);
	   $this->fecha   = $a_fecha;
	   
	}

	
###Setters.	
    public function setTitulo($title)
    {
	    $this->titulo = $title;
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
	public function getTitulo()
	{
		return $this->titulo;
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
	
	
###Verifications.
 public function existArticulo($con)
 {
   $query = "SELECT * FROM articulos_colab WHERE titulo = '" . $this->getTitulo() . "' ";
   $rs = $con->Execute($query) or die("<p class=\"error_msg\">Error accediendo a la base de datos!</p>");
   
   $exist = $rs->RecordCount();
   
   if( $exist != '0' ) {return true;}
   else {return false;}
   
 } 
	
	
###CRUDs.	
public function saveArticulo($con)
{
    if(!$this->existArticulo($con)){
	
    $saveQuery = " INSERT INTO articulos_colab (titulo, autor, cuerpo, fecha) VALUES ( '" . $this->getTitulo() . "','".$this->getAutor()."','" . $this->getCuerpo() . "','" . $this->getFecha() . "'   ) ";
								 							 
	$rs = $con->Execute($saveQuery) or die("<p class=\"error_msg\">Error accediendo a la base de datos!</p>");  						
	
	   return true;	 
	}
    else
     { 
	   return false;
	 }
  
}


 
}
 
?>
