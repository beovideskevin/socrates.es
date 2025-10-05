/**
 * Usage:

    <p> Para leer mas detalles
        <button  class="note-button fa fa-plus" data-note="note1"></button>
        <blockquote id="note1" class="note-wrapper">29. Thomson, George, “Los Primeros Filósofos”, Edit. Edición Revolucionaria, Instituto del Libro, La Habana 1968.</blockquote> 
    </p>
 */
document.addEventListener("DOMContentLoaded", () => {
    $(".note-wrapper").each((index, note) => {
        $(note).hide();
    });

    $(".note-button").on('click', function() {
        const id = $(this).attr("data-note");
        $(`#${id}`).show();
        $(this).hide();
    });
});