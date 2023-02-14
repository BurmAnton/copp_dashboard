document.addEventListener('DOMContentLoaded', function() {
  const input = document.querySelector('#id_import_file').classList;
  console.log(input);
  input.add('form-control');

  document.querySelector('.edit-icon').addEventListener('click', (btn) => {
      document.querySelectorAll('.delete-participant').forEach(element =>{
          if (element.style.display === "none") {
              element.style.display = "table-cell";
            } else {
              element.style.display = "none";
            }
      });
      document.querySelector('.edit-icon').classList.toggle("clicked");
  })
})
