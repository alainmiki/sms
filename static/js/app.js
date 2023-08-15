
// import "./dist/jspdf.umd"

function generatePDF() {
  var doc = new jsPDF(); //create jsPDF object
  doc.
  doc.fromHTML(
    document.getElementById("test"), // page element which you want to print as PDF
    15,
    15,
    {
      width: 170, //set width
    },
    function (a) {
      doc.save("HTML2PDF.pdf"); // save file name as HTML2PDF.pdf
    }
  );
}


function getiImg2Display(event) {
  src = URL.createObjectURL(event.target.files[0]);
  const images = document.getElementById("imgdisplay");
  images.src = src;
  image_url = src;
  // console.log(src);
  
}


console.log(document.getElementById("test"));
generatePDF();

console.log("miki");